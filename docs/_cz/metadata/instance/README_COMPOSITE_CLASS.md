# 🧩 Kompozitní instance — `make_composite_class` a reaktivní jádro

Kompozitní instance staví přímo na atomické (viz
[README_ATOM_CLASS.md](README_ATOM_CLASS.md)) — dědí od ní, ne od
`InstanceBase` znovu. Tenhle dokument popisuje, jak se kompozice sestaví
a jak funguje obousměrná reaktivita, o které mluví úvodní koncept
knihovny.

```
InstanceBase
└── {Meta.owner_class}AtomBase           (atomický základ)
    └── {Meta.owner_class}CompositeBase  ← vytváří make_composite_class
```

---

## 🧭 Obsah

* [`make_composite_class` — kompilace kompozitní třídy](#make_composite_class--kompilace-kompozitní-třídy)
* [`_get_inner_instance_class` — výběr třídy pro vnitřní prvek](#_get_inner_instance_class--výběr-třídy-pro-vnitřní-prvek)
* [`create_composite_init` — konstruktor](#create_composite_init--konstruktor)
* [`create_properties_for_inners` — přístup k vnitřním prvkům](#create_properties_for_inners--přístup-k-vnitřním-prvkům)
* [`create_recalculate_self` — tok hodnot nahoru](#create_recalculate_self--tok-hodnot-nahoru)
* [`create_recalculate_inners` — tok hodnot dolů](#create_recalculate_inners--tok-hodnot-dolů)
* [Reaktivita jako celek](#reaktivita-jako-celek)

---

## `make_composite_class` — kompilace kompozitní třídy

**Parametry:** `meta`, `mutable` (výchozí `True`).

**Návratová hodnota:** dynamicky vytvořená třída (`CompositeInstanceProtocol`).

**Pod kapotou (zkráceně):**
```python
def make_composite_class(meta, *, mutable=True):
    base_class_name = f"{meta.class_name}Composite{'Mutable' if mutable else 'Immutable'}Base"
    base_class = meta.atom_class_mutable if mutable else meta.atom_class_immutable
    class_parents = (base_class,)

    class_dict = {
        "__metadata__": meta,
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name, mutable=mutable),
        "value": create_value_property(meta, is_constant=False, mutable=mutable),
    }
    class_dict |= create_properties_for_inners(meta, mutable=mutable)

    if mutable:
        class_dict["_recalculate_self"] = create_recalculate_self(meta, base_class_name)
        class_dict["_recalculate_inners"] = create_recalculate_inners(meta, base_class_name)

    composite_class = type(base_class_name, class_parents, class_dict)

    for name in ("inners", "_logic", "_decompose"):
        if name in composite_class.__dict__:
            delattr(composite_class, name)

    return composite_class
```

**Jediný rodič — atomická třída.** `class_parents = (base_class,)`, kde
`base_class` je právě zkompilovaná `atom_class_mutable`/`_immutable`.
Kompozice tedy **je** atom (dědí `_value`, `_owner`, `_locked`,
`_root_value_setter`, `init_mixins`, `meta`...) a navrch přidává vlastní
strukturu. Tohle je přesně ten mechanismus, díky kterému může mít
kompozice i vlastní `value` (přepsané níže na kompozitní chování) a
zároveň zůstat kompatibilní se vším, co počítá s atomickým rozhraním
(např. `_root_value_setter` volané z `_recalculate_inners` rodiče).

**Sloty jsou odvozené přímo z `_inners`** —
`tuple(inner.meta.name_private for inner in meta.inners)` — každý vnitřní
prvek dostane vlastní privátní slot (např. `_engine`, `_wheels`), do
kterého se uloží jeho **instance** (ne hodnota — instance).

**Reaktivní hooky jen pro mutable.** `_recalculate_self` a
`_recalculate_inners` (viz níže) dávají smysl jen tam, kde se hodnoty
vůbec mohou měnit — immutable kompozice je po inicializaci strukturálně
zamrzlá.

**Cleanup na konci** stejně jako u atomů — odstraní se `inners`, `_logic`,
`_decompose`, aby instance nevystavovala schéma blueprintu.

[▲ Nahoru](#-obsah)

---

## `_get_inner_instance_class` — výběr třídy pro vnitřní prvek

**Parametry:** `inner_meta`, `mutable`.

**Návratová hodnota:** správná instanční třída pro daný vnitřní prvek.

**Pod kapotou:**
```python
def _get_inner_instance_class(inner_meta, mutable):
    if mutable:
        return inner_meta.atom_class_mutable if inner_meta.is_constant else inner_meta.composite_class_mutable
    return inner_meta.atom_class_immutable if inner_meta.is_constant else inner_meta.composite_class_immutable
```

Malá, ale důležitá rozhodovací matice 2×2 (mutable/immutable ×
constant/composite) — vnitřní prvek kompozice může sám být buď atom, nebo
další kompozice (rekurzivní vnořování do libovolné hloubky), a tahle
funkce zajišťuje, že se pro něj vybere přesně ta správná ze čtyř
variant. Přístup přes `inner_meta.atom_class_mutable` atd. zároveň
**spouští líné vytvoření** té třídy, pokud ještě neexistuje (viz
[README_SIMPLE_CONSTANT_METADATA.md](README_SIMPLE_CONSTANT_METADATA.md#líné-vytváření-atomických-tříd)) —
takže i hluboko zanořené stromy kompozic se kompilují efektivně, jen na
vyžádání.

[▲ Nahoru](#-obsah)

---

## `create_composite_init` — konstruktor

**Parametry:** `meta`, `base_class_name`, `mutable` (výchozí `True`).

**Návratová hodnota:** funkce `__init__` jako closure.

**Pod kapotou:**
```python
def create_composite_init(meta, base_class_name, *, mutable=True):
    def __init__(self):
        for inner in meta.inners:
            inner_meta = inner.meta
            inner_cls = _get_inner_instance_class(inner_meta, mutable)
            inner_instance = object.__new__(inner_cls)
            inner_instance.__init__()
            inner_instance._owner = self
            setattr(self, inner_meta.name_private, inner_instance)

        if mutable:
            meta.atom_class_mutable.__init__(self)
        else:
            meta.atom_class_immutable.__init__(self)

    ...
    return __init__
```

**Přísně dané pořadí kroků — a není náhodné.** Nejdřív se vytvoří a
napojí **všechny vnitřní prvky**, teprve pak se zavolá inicializace
atomické vrstvy (`meta.atom_class_mutable.__init__(self)`, což mimo jiné
spustí `init_mixins`). Důvod: mixiny inicializované v atomické fázi
(typicky strukturální, jako `NodesTuple`/`NodesDicts` — viz sekce mixinů)
očekávají, že strom vnitřních prvků je **už kompletní**, když se
spustí. Kdyby se pořadí prohodilo, tyhle mixiny by narazily na chybějící
sloty.

**Vytváření vnitřních instancí obchází `SimpleMeta.__call__` úplně
záměrně** — `object.__new__(inner_cls)` + ruční `inner_instance.__init__()`
místo prostého zavolání `inner_cls()`. Kdyby se totiž zavolalo
`inner_cls()`, prošlo by to metaclassou (protože `inner_cls` je pořád
třída se `SimpleMeta`) a `SimpleMeta.__call__` by spustilo **celou**
`create_instance` pipeline znovu — zbytečně a nesprávně, protože `inner_cls`
už je hotová, zkompilovaná runtime třída, ne blueprint.

**`_owner` propojení je obousměrný vztah** — `inner_instance._owner = self`
dává vnitřnímu prvku odkaz na rodiče, což je přesně to, co `_root_value_setter`
potřebuje pro bublání změn nahoru (viz
[README_ATOM_CLASS.md](README_ATOM_CLASS.md#create_root_value_setter--reaktivní-zápis-hodnoty)).

**Bez `super()`.** Komentář v `_DESIGN_NOTES` zdrojáku to zdůvodňuje jasně:
explicitní volání (`meta.atom_class_mutable.__init__(self)`) je
deterministické a nezávislé na MRO, zatímco `super()` by v dynamicky
skládané hierarchii tříd mohl vést k nejasnému pořadí volání.

[▲ Nahoru](#-obsah)

---

## `create_properties_for_inners` — přístup k vnitřním prvkům

**Parametry:** `meta`, `mutable` (výchozí `True`).

**Návratová hodnota:** `dict` — properties pro sloučení do `class_dict`.

**Pod kapotou:**
```python
def create_properties_for_inners(meta, *, mutable=True):
    return {
        k: v
        for inner in meta.inners
        for k, v in create_properties_for_inner(inner.meta, path=(), mutable=mutable).items()
    }
```

Pro každý přímý vnitřní prvek vygeneruje **dvě** properties (detailní popis
mechaniky je v [README_VALUE_PROPERTIES.md](README_VALUE_PROPERTIES.md)):
`<jméno>` pro přístup k hodnotě a `<jméno>_instance` pro přístup k samotné
instanci. Výsledek se do `class_dict` sloučí přes `|=` — properties tedy
vznikají **při kompilaci třídy**, ne za běhu přes `setattr` smyčku, což je
rychlejší a umožňuje to statickou introspekci (`dir(instance)` ukáže
všechny properties hned).

[▲ Nahoru](#-obsah)

---

## `create_recalculate_self` — tok hodnot nahoru

**Parametry:** `meta`, `base_class_name`.

**Návratová hodnota:** funkce `_recalculate_self` jako closure. Jen pro
mutable varianty.

**Pod kapotou:**
```python
def create_recalculate_self(meta, base_class_name):
    def _recalculate_self(self):
        current_values = {
            inner.meta.name_snake: getattr(self, inner.meta.name_private).value
            for inner in meta.inners
        }
        new_value = self.calculate_value(**current_values)

        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        self._value = new_value

        if self._owner:
            self._owner._recalculate_self()

    ...
    return _recalculate_self
```

Tohle je odpověď na otázku "co se stane, když se změní hodnota **uvnitř**
kompozice" (🔼 z úvodního konceptu):

1. **Sesbírej aktuální hodnoty všech přímých dětí** do `{jméno: hodnota}`
   mapy — přesně formát, který `calculate_value` (respektive
   `_process_calculate_value_params`) očekává jako kwargs.
2. **Přepočítej** — zavolá se veřejné `self.calculate_value(**current_values)`,
   tedy stejná metoda, kterou by zavolal i uživatel ručně (viz
   [README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#calculate_value)).
3. **Short-circuit při shodě** — stejný vzor jako u `_root_value_setter`,
   tady navíc obalený v `try/except`, protože porovnání (`==`) nemusí být
   u libovolného typu bezpečné.
4. **Zápis a bublání dál nahoru** — pokud se hodnota změnila, uloží se a
   (pokud existuje vlastník) zavolá se `_recalculate_self` na **rodiči
   téhle kompozice** — řetězec se táhne až k nejvyššímu kořeni stromu.

[▲ Nahoru](#-obsah)

---

## `create_recalculate_inners` — tok hodnot dolů

**Parametry:** `meta`, `base_class_name`.

**Návratová hodnota:** funkce `_recalculate_inners` jako closure. Jen pro
mutable varianty.

**Pod kapotou:**
```python
def create_recalculate_inners(meta, base_class_name):
    def _recalculate_inners(self):
        decomposed = self.decompose_value(self._value)

        for inner, inner_value in zip(meta.inners, decomposed):
            inner_instance = getattr(self, inner.meta.name_private)
            inner_instance._root_value_setter(inner_value, recalculate_up=False)

            if not inner.meta.is_constant:
                inner_instance._recalculate_inners()

    ...
    return _recalculate_inners
```

Opačný směr (🔽 z úvodního konceptu) — "co se stane, když se změní hodnota
**celé** kompozice":

1. **Dekompoň** — `self.decompose_value(self._value)` rozloží aktuální
   hodnotu na díly pro jednotlivé `_inners` (viz
   [README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#decompose_value)).
2. **Rozešli díly dětem** — pro každý vnitřní prvek se zavolá jeho
   `_root_value_setter` s **`recalculate_up=False`** — tohle je klíčové:
   bez toho by zápis do dítěte okamžitě spustil `_recalculate_self`
   zpátky na rodiči, což by vytvořilo nekonečnou smyčku (dolů → nahoru →
   dolů → ...).
3. **Kaskáda do vnořených kompozic** — pokud je vnitřní prvek sám další
   kompozice (`not inner.meta.is_constant`), zavolá se na něm rekurzivně
   `_recalculate_inners()`, aby se rozklad propagoval do libovolné
   hloubky stromu.

**`zip(meta.inners, decomposed)` vynucuje striktní poziční shodu** — proto
`verify_decompose_outcome` (viz
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md#verify_decompose_outcome--speciální-pravidla-pro-_decompose))
kontroluje, že `_decompose` vrací tuple přesně stejné délky a pořadí jako
`_inners`.

[▲ Nahoru](#-obsah)

---

## Reaktivita jako celek

Obě reaktivní metody dohromady tvoří uzavřený, bezpečný cyklus:

```
zápis do vnitřního prvku (_root_value_setter, recalculate_up=True)
        │
        ▼
  _recalculate_self  (na rodiči, může bublat dál nahoru)
        │
zápis do kompozice (value = ..., přes create_value_setter)
        │
        ▼
  _recalculate_inners  (rozešle recalculate_up=False dětem)
```

Klíčový bezpečnostní mechanismus proti nekonečným smyčkám je vždy stejný:
**směr, kterým se změna právě šíří, si nese `recalculate_up=False`**, aby
se nemohla "odrazit" zpátky. Kombinace se short-circuit kontrolami
(hodnota se nezměnila → žádné další šíření) navíc zaručuje, že i rozsáhlý
strom kompozic reaguje na jedinou změnu jen minimálním nutným počtem
přepočtů.

➡️ Pokračování: [README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md)

[▲ Nahoru](#-obsah)
