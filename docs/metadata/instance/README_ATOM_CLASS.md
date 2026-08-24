# ⚛️ Atomická instance — `make_atom_class` a její stavební bloky

Tenhle dokument popisuje, jak se z blueprintu (`SimpleConstant`/`SimpleObject`
třídy) stane **skutečná, běžící atomická instance** — nejmenší strukturální
jednotka celého systému. Kompozitní instance (viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md)) na ní přímo staví
dědičností.

```
InstanceBase                        (identita, sloty, meta property)
└── {Meta.owner_class}AtomBase      ← vytváří make_atom_class
```

---

## 🧭 Obsah

* [`InstanceBase` — společný kořen všech instancí](#instancebase--společný-kořen-všech-instancí)
* [`make_atom_class` — kompilace atomické třídy](#make_atom_class--kompilace-atomické-třídy)
* [`create_atom_init` — konstruktor](#create_atom_init--konstruktor)
* [`create_root_value_setter` — reaktivní zápis hodnoty](#create_root_value_setter--reaktivní-zápis-hodnoty)

---

## `InstanceBase` — společný kořen všech instancí

Než se podíváme na `make_atom_class`, stojí za připomenutí, co dává
`InstanceBase` (viz i [README_SIMPLE_META.md](README_SIMPLE_META.md#odkud-se-berou-skutečné-runtime-třídy))
úplně **každé** instanci — atomické i kompozitní:

```python
class InstanceBase:
    _is_instance_class: bool = True
    __slots__ = ("__weakref__",)

    def init_mixins(self) -> None: ...

    @property
    def meta(self) -> "SimpleMetadataLike":
        return self.__class__.__metadata__

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
```

* **`_is_instance_class = True`** — signál pro `SimpleMeta.__new__`, aby
  dynamicky vytvořenou třídu nebral jako nový blueprint (viz
  [README_SIMPLE_META.md](README_SIMPLE_META.md#__new__--vznik-třídy)).
* **`__slots__ = ("__weakref__",)`** — žádný `__dict__`, jen podpora slabých
  referencí. Ostatní sloty (`_value`, `_owner`, `_locked`...) přidává až
  konkrétní atomická/kompozitní třída.
* **`init_mixins`** — prázdný default, přepsaný/rozšířený dynamicky přes
  `_build_combined_init_mixins` (viz
  [README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_build_combined_init_mixins)),
  pokud instance obsahuje mixiny s vlastní inicializací.
* **`meta`** — konstantní přístup k metadatům přímo z třídy instance
  (`self.__class__.__metadata__`), ne přes žádné vyhledávání.

[▲ Nahoru](#-obsah)

---

## `make_atom_class` — kompilace atomické třídy

**Parametry:**
* `meta` (*SimpleMetadataLike*): metadata blueprintu.
* `mutable` (*bool*, výchozí `True`): mutable, nebo immutable varianta.

**Návratová hodnota:** dynamicky vytvořená třída (`AtomInstanceProtocol`).

**Pod kapotou (zkráceně):**
```python
def make_atom_class(meta, *, mutable=True):
    base_class_name = f"{meta.class_name}Atom{'Mutable' if mutable else 'Immutable'}Base"
    class_parents = (InstanceBase, meta.owner_class)

    class_dict = {
        "_is_mutable": mutable,
        "__metadata__": meta,
        "__slots__": ("_value", "_owner", "_locked"),
        "__init__": create_atom_init(meta, base_class_name),
        "value": create_value_property(meta, mutable=mutable),
        "owner": property(lambda self: self._owner),
    }
    if mutable:
        class_dict["_root_value_setter"] = create_root_value_setter(base_class_name)

    atom_class = type(base_class_name, class_parents, class_dict)

    for name in ("_type", "_default", "_validate", "bool_or_raise_validate_error"):
        if name in atom_class.__dict__:
            delattr(atom_class, name)

    return atom_class
```

**Dvojí dědičnost je záměrná.** `class_parents = (InstanceBase,
meta.owner_class)` — instance dědí jak strukturální identitu
(`InstanceBase`), tak **doménové chování z blueprintu samotného**
(`meta.owner_class`, tedy třída, kterou napsal uživatel — se svou
`_validate`, případně dalšími metodami). Instance tak "je" tou uživatelskou
třídou i strukturálně kompatibilní runtime objekt zároveň.

**Sloty `_value`, `_owner`, `_locked`** — tři pole, která stačí na
kompletní atomický stav: aktuální hodnota, odkaz na rodiče v kompozici
(pro bublání změn nahoru), a příznak immutability.

**Cleanup na konci je stejně důležitý jako sestavení.** Po vytvoření třídy
se z ní **odstraní deklarativní artefakty** (`_type`, `_default`,
`_validate`, `bool_or_raise_validate_error`) — instance nemá přístup ke
schématu blueprintu, jen k výsledku. Uživatel, který drží v ruce instanci,
tak nevidí "definiční" API — jen runtime API (`value`, `owner`, případně
metody z mixinů).

[▲ Nahoru](#-obsah)

---

## `create_atom_init` — konstruktor

**Parametry:** `meta`, `base_class_name` (pro `__qualname__`).

**Návratová hodnota:** funkce `__init__` jako closure.

**Pod kapotou:**
```python
def create_atom_init(meta, base_class_name):
    def __init__(self):
        self._value = meta.default
        self._owner = UNSET
        self._locked = False
        self.init_mixins()

    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    return __init__
```

**Closure místo obyčejné metody** — `meta` je zachycená v uzávěru, takže
konstruktor nemusí při každém vytvoření instance dohledávat metadata znovu
(`self.meta` by šlo taky, ale closure je rychlejší a přímočařejší, protože
`meta` je v okamžiku kompilace třídy už definitivně známá).

**Reflection alignment** (`__name__`, `__qualname__`) — bez tohohle kroku
by dynamicky vytvořená funkce v tracebacku vypadala jako anonymní
"`<locals>.__init__`". Přepsáním těchto atributů vypadá `__init__` v
diagnostice jako **nativní člen generované třídy** — důležité pro
ladění, protože celý systém běžně vytváří desítky dynamických tříd.

Instance vždy startuje s **výchozí hodnotou z metadat** (`meta.default`),
bez vlastníka (`_owner = UNSET`) a odemčená (`_locked = False`) — vlastnictví
se přiřazuje až zvenčí, když se instance stane vnitřním prvkem kompozice
(viz [README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_composite_init--konstruktor)).

Poslední krok, `self.init_mixins()`, je hák, na kterém stojí celá
rozšiřitelnost mixiny — v základní atomické třídě je to prázdná metoda z
`InstanceBase`, ale jakmile jsou přidané mixiny s vlastní inicializací,
`create_instance_class` ji nahradí sloučeným řetězem volání (viz
[README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md#_build_combined_init_mixins)).

[▲ Nahoru](#-obsah)

---

## `create_root_value_setter` — reaktivní zápis hodnoty

**Parametry:** `base_class_name`.

**Návratová hodnota:** funkce `_root_value_setter` jako closure. Existuje
jen na **mutable** variantě — immutable instance ji vůbec nemá.

**Pod kapotou:**
```python
def create_root_value_setter(base_class_name):
    def _root_value_setter(self, value, recalculate_up=True):
        new_value = self.normalize(value, process_none=True)

        if self._value == new_value:
            return

        self._value = new_value

        if self._owner and recalculate_up:
            self._owner._recalculate_self()

    ...
    return _root_value_setter
```

Tohle je **skutečné srdce reaktivity směrem nahoru** ("🔼" z úvodního
konceptu knihovny). Čtyři kroky:

1. **Normalizace** — vstup vždy projde `self.normalize(value,
   process_none=True)`, takže `None` je automaticky nahrazeno defaultem
   místo vyhození chyby (na rozdíl od veřejného `value` setteru, kde
   `None` typicky chyba je — tohle je interní, permisivnější varianta pro
   reaktivní propagaci).
2. **Short-circuit při shodě** — pokud se nová hodnota rovná staré, funkce
   skončí okamžitě. Tohle je klíčová optimalizace: bez ní by každá byť
   nulová změna spustila celou kaskádu přepočtů směrem nahoru.
3. **Zápis** — `self._value = new_value`.
4. **Bublání nahoru** — jen pokud instance **má** vlastníka (`self._owner`
   není `UNSET`) **a** je povolené bublání (`recalculate_up=True`),
   zavolá se `self._owner._recalculate_self()`.

**Parametr `recalculate_up` je záměrně přepínatelný**, protože
`_root_value_setter` se používá ve dvou různých směrech: veřejný zápis
hodnoty (`value = ...`, kde bublání dává smysl) a vnitřní distribuce
hodnot směrem dolů z `_recalculate_inners` (viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_recalculate_inners--tok-hodnot-dolů)),
kde by bublání zpátky nahoru vytvořilo nekonečnou smyčku — proto se tam
volá s `recalculate_up=False`.

[▲ Nahoru](#-obsah)

➡️ Pokračování: [README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md)
