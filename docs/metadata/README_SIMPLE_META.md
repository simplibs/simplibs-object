# 🧠 `SimpleMeta` — Metaclass, která řídí celý životní cyklus

`SimpleMeta` je mozek celého Simple systému. Zatímco `SimpleBase`,
`SimpleConstant` a `SimpleObject` popisují, *co* uživatel smí deklarovat,
`SimpleMeta` řídí, *co se s tím stane* — od okamžiku definice třídy až po
vytvoření běžící instance.

```
SimpleBase(metaclass=SimpleMeta)
└── SimpleConstant
    └── SimpleObject
```

Metaclass se stará o pět věcí, v tomhle pořadí (a není to náhoda — kopíruje
to přirozený životní cyklus třídy: vznik → ochrana → instanciace →
reprezentace → přístup k metadatům):

1. [`__new__`](#__new__--vznik-třídy) — vznik třídy a napojení metadat
2. [`__setattr__`](#__setattr__--write-once-ochrana) — write-once ochrana
3. [`__call__`](#__call__--vytváření-instancí) — vytváření instancí
4. [`__repr__` a `__str__`](#__repr__-a-__str__--reprezentace) — reprezentace
5. [`meta`](#meta--přístup-k-metadatům) — přístup k metadatům

---

## 🧭 Obsah

* [`__new__` — vznik třídy](#__new__--vznik-třídy)
* [`__setattr__` — write-once ochrana](#__setattr__--write-once-ochrana)
* [`__call__` — vytváření instancí](#__call__--vytváření-instancí)
* [`__repr__` a `__str__` — reprezentace](#__repr__-a-__str__--reprezentace)
* [`meta` — přístup k metadatům](#meta--přístup-k-metadatům)
* [Doporučené pořadí dunder metod](#doporučené-pořadí-dunder-metod)

---

## `__new__` — vznik třídy

Spouští se v okamžiku, kdy Python načítá definici nové třídy (`class Age(SimpleConstant): ...`).

```python
def __new__(mcls, name, bases, namespace):
    cls = super().__new__(mcls, name, bases, namespace)

    if hasattr(cls, "_is_instance_class") or name in BASE_CLASS_NAMES:
        return cls

    calculated_metadata = (
        SimpleObjectMetadata(owner_class=cls)
        if hasattr(cls, "_inners")
        else SimpleConstantMetadata(owner_class=cls)
    )
    cls.__metadata__ = calculated_metadata

    return cls
```

Tři důležité detaily:

**1. Rozlišení konstanta vs. kompozice je jediný `hasattr` check.** Systém
nikde nenutí uživatele explicitně říct "tohle je kompozice" — stačí, že
třída definuje `_inners`, a metaclass sama pozná, že potřebuje
`SimpleObjectMetadata` místo `SimpleConstantMetadata`. Jednoduché, ale
elegantní rozhodovací pravidlo.

**2. Dvojí guard proti nekonečné rekurzi / zbytečné práci.** `name in
BASE_CLASS_NAMES` přeskočí systémové třídy (`SimpleBase`, `SimpleConstant`,
`SimpleObject` samotné — ty žádná metadata mít nemají). `hasattr(cls,
"_is_instance_class")` přeskočí **dynamicky vytvořené runtime třídy**
(atomické a kompozitní instance vytvořené přes `make_atom_class`/
`make_composite_class`) — ty totiž procházejí stejnou metaclassou
(dědí `_type`/`_inners` atd. z blueprintu), ale metadata už mají hotová
a nový výpočet by byl zbytečný i chybný. Tohle je přesně to místo, kde se
setkává deklarativní svět (blueprinty) s runtime světem (instance).

**3. Metadata se počítají jednou a natvrdo se přilepí na třídu.**
`cls.__metadata__ = calculated_metadata` — od teď je metadata pro danou
třídu hotová, spočítaná a (díky `__setattr__` níže) neměnná.

[▲ Nahoru](#-obsah)

---

## `__setattr__` — write-once ochrana

Spouští se při **každém** přiřazení atributu na úrovni třídy.

```python
def __setattr__(cls, attr_name, new_value):
    if attr_name in cls.__dict__:
        raise_attribut_allready_set(cls, attr_name, new_value)
    super().__setattr__(attr_name, new_value)
```

Kontrola je záměrně `attr_name in cls.__dict__`, ne `getattr(cls,
attr_name, UNSET) is not UNSET` (viz zakomentovaný řádek v kódu) —
rozdíl je důležitý: `cls.__dict__` hlídá jen atributy definované **přímo
na téhle třídě**, ne zděděné. Kdyby se kontrolovalo přes `getattr`, nešlo
by v podtřídě vůbec nic nastavit, protože by to vždy narazilo na zděděnou
hodnotu z rodiče.

**Proč blueprint musí být write-once:** jakmile jednou proběhne
`__new__` a spočítají se metadata, celý zbytek systému (validace, výpočet
defaultů, instance builders) spoléhá na to, že se definice třídy už nikdy
nezmění. Kdyby šlo za běhu přepsat `_type` nebo `_default`, metadata by
okamžitě zastarala a nikdo by o tom nevěděl. Write-once ochrana tohle
riziko úplně eliminuje — jakýkoliv pokus o přepsání je okamžitá,
srozumitelná chyba místo tichého nekonzistentního stavu.

[▲ Nahoru](#-obsah)

---

## `__call__` — vytváření instancí

Spouští se, když se blueprint třída *zavolá jako funkce*
(`Age()`, `Person(mutable=False)`).

```python
def __call__(cls, *, mixins=(), as_atom=False, mutable=True):
    return create_instance(cls, mixins=mixins, as_atom=as_atom, mutable=mutable)
```

Sama `SimpleMeta` tady žádnou logiku neobsahuje — jen deleguje na
`create_instance`, což je samostatný, mnohem komplexnější orchestrátor
celého vytváření instance. Stručný přehled toho, co se pod kapotou stane
(detailní dokumentace bude v samostatném README pro instance buildery):

1. **Validace vstupu** — `cls` nesmí být systémová base třída, `as_atom`
   a `mutable` musí být `bool`.
2. **Rozhodnutí atom vs. composite** (`is_atom = cls.meta.is_constant or
   as_atom`) — konstanta je vždy atom, kompozice může být vynucena do
   atomického chování přes `as_atom=True`.
3. **Kontrola hashovatelnosti pro immutable** — immutable hodnota musí
   být hashovatelná, jinak by nedávala smysl jako neměnná.
4. **Výběr strukturální base třídy** (`get_base_class`) — vybírá se
   z kombinace atom/composite × mutable/immutable.
5. **Kompilace finální runtime třídy** (`create_instance_class`) —
   zpracování mixinů, sestavení namespace, sloty, rozšiřující hooky.
6. **Alokace syrové paměti** přes `object.__new__` — bez předčasného
   spuštění `__init__` rodičovských tříd.
7. **Inicializace** (`instance.__init__()`).
8. **Vrácení hotové instance.**

Klíčová myšlenka je **dvoufázová konstrukce**: nejdřív se jednou zkompiluje
runtime třída (`create_instance_class`), teprve pak se z ní alokuje
instance. Tohle oddělení znamená, že dynamická tvorba třídy (ta drahá
část) proběhne jednou za spuštění dané kombinace parametrů, ne opakovaně
pro každou jednotlivou instanci.

### Odkud se berou skutečné runtime třídy

`create_instance` interně sahá po dvou "továrnách", které žijí
v `_core/metadata/instance_builders/`:

* **`make_atom_class(meta, mutable=...)`** — vytvoří atomickou instanční
  třídu. Dědí ze dvou rodičů: `InstanceBase` (identita, `_is_instance_class`,
  sloty, přístup k metadatům) a `meta.owner_class` (doménové chování
  z blueprintu). Přidá sloty `_value`, `_owner`, `_locked`, hotový
  `__init__`, `value` property, a u mutable varianty i
  `_root_value_setter` pro reaktivní zápis. Nakonec **odstraní deklarativní
  artefakty** (`_type`, `_default`, `_validate`, ...) — instance nemá
  přístup ke schématu, jen k výsledku.
* **`make_composite_class(meta, mutable=...)`** — postaví kompozitní
  instanční třídu **nad atomickou** (`class_parents = (base_class,)`, kde
  `base_class` je právě `atom_class_mutable`/`atom_class_immutable`). Přidá
  slot pro každý vnitřní prvek (`inner.meta.name_private`), properties pro
  přístup k jednotlivým `_inners`, a u mutable varianty reaktivní hooky
  `_recalculate_self` a `_recalculate_inners` — tohle je přesně ten
  mechanismus, který dělá ze změny v jednom vnitřním prvku okamžitý
  přepočet celé kompozice.

Obě funkce sdílejí stejný vzor: **sestav jméno → vyber rodiče → postav
`class_dict` → `type(name, bases, dict)` → ukliď deklarativní zbytky.**
Použití `type(...)` místo `exec` drží celou kompilaci bezpečnou
a explicitní — žádný generovaný zdrojový kód, žádné parsování řetězců.

A `InstanceBase` je společný kořen obou — dává jim `_is_instance_class =
True` (aby je `SimpleMeta.__new__` nebral jako nové blueprinty, viz výše),
`__slots__ = ("__weakref__",)` (žádný `__dict__`, podpora weak referencí),
rychlý přístup k metadatům (`meta` property čte přímo `__metadata__`
z třídy) a diagnostické `__repr__`/`__str__`.

[▲ Nahoru](#-obsah)

---

## `__repr__` a `__str__` — reprezentace

```python
def __repr__(cls):
    return (
        f"<class {cls.__name__} (System Base)>"
        if cls.meta is UNSET else
        f"<{cls.meta.class_name}Blueprint blueprint='{cls.meta.blueprint_path}' "
        f"type={'Constant' if cls.meta.is_constant else 'Object'}>"
    )

def __str__(cls):
    return cls.__name__
```

`__repr__` je technická, ladicí reprezentace **blueprintu** (ne instance) —
ukazuje cestu v hierarchii a jestli jde o konstantu, nebo kompozici.
`__str__` je záměrně strohé — jen čisté jméno třídy, vhodné pro logy
a uživatelsky čitelné výstupy.

[▲ Nahoru](#-obsah)

---

## `meta` — přístup k metadatům

```python
@property
def meta(cls) -> "SimpleMetadataLike":
    return cls.__metadata__
```

Stabilní veřejné rozhraní k metadatům — všude v systému (validace,
`calculate_value`, `decompose_value`, instance buildery) se sahá přes
`cls.meta`, nikdy přímo přes `cls.__metadata__`. Tahle jedna úroveň
indirection znamená, že se interní úložiště metadat může v budoucnu změnit,
aniž by se muselo přepisovat cokoliv jiného v knihovně.

[▲ Nahoru](#-obsah)

---

## Doporučené pořadí dunder metod

Pořadí použité v `SimpleMeta` (`__new__` → `__setattr__` → `__call__` →
`__repr__` → `__str__` → `meta`) odpovídá přirozenému životnímu cyklu
třídy: **vznik → ochrana → instanciace → reprezentace → přístup k
metadatům.** Je to zároveň pořadí, které používá CPython u vlastních
metaclassů i většina zavedených frameworků — takže se dá brát jako
doporučená konvence i pro další metaclassy v ekosystému.

➡️ Hlubší dokumentace k metadatům a vytváření instancí (`SimpleBaseMetadata`,
`SimpleConstantMetadata`, `SimpleObjectMetadata`, `make_atom_class`,
`make_composite_class`, `create_instance`) bude v navazujícím README, až se
k této sekci dostaneme podle osnovy.

[▲ Nahoru](#-obsah)
