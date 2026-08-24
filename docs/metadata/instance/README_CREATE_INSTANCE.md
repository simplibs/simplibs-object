# 🏗️ `create_instance` — Orchestrace a mixin pipeline

Tenhle dokument popisuje nejvyšší úroveň vytváření instance — to, co se
skutečně spustí, když zavoláš `MyClass(mixins=(...), mutable=False)`, tedy
přesně to, na co deleguje `SimpleMeta.__call__` (viz
[README_SIMPLE_META.md](README_SIMPLE_META.md#__call__--vytváření-instancí)).
Zatímco [README_ATOM_CLASS.md](README_ATOM_CLASS.md) a
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md) popisují strukturální
základ (atom/kompozice), tenhle dokument popisuje, jak se na ten základ
**bezpečně nalepí mixiny**.

---

## 🧭 Obsah

* [`create_instance` — hlavní orchestrátor](#create_instance--hlavní-orchestrátor)
* [`get_base_class` — výběr strukturálního základu](#get_base_class--výběr-strukturálního-základu)
* [`create_instance_class` — kompilace finální třídy](#create_instance_class--kompilace-finální-třídy)
* [`_resolve_flat_mixins` — zploštění hierarchie mixinů](#_resolve_flat_mixins--zploštění-hierarchie-mixinů)
* [`_verify_mixin_compatibility` — kompatibilní matice](#_verify_mixin_compatibility--kompatibilní-matice)
* [`_build_instance_class_dict` — namespace injection](#_build_instance_class_dict--namespace-injection)
* [`_build_combined_init_mixins` — řetězení inicializace](#_build_combined_init_mixins--řetězení-inicializace)
* [`_extend_instance_class` — post-kompilační hooky](#_extend_instance_class--post-kompilační-hooky)

---

## `create_instance` — hlavní orchestrátor

**Parametry:** `cls`, `mixins` (tuple), `as_atom` (bool), `mutable` (bool, výchozí `True`).

**Návratová hodnota:** hotová, inicializovaná instance.

**Osm kroků pipeline:**

```
1. Validace vstupu (cls není base class, as_atom/mutable jsou bool)
2. is_atom = cls.meta.is_constant or as_atom
3. Kontrola hashovatelnosti (jen pro immutable)
4. get_base_class  ──► vybere strukturální základ
5. create_instance_class  ──► zkompiluje finální třídu s mixiny
6. object.__new__  ──► alokace syrové paměti
7. instance.__init__()  ──► inicializace
8. return instance
```

**Krok 2 je jednořádkové, ale důležité pravidlo:** `is_atom = cls.meta.is_constant
or as_atom` — konstanta je **vždy** atom, bez ohledu na `as_atom`; kompozici
lze naopak vynutit do atomického chování (`as_atom=True`), pokud by pro
nějaký účel dávalo smysl zacházet s ní jako s jedním kusem hodnoty místo
strukturovaného stromu.

**Krok 3 — immutable musí být hashovatelná.** Dává smysl: pokud je hodnota
neměnná, měla by fungovat jako klíč v `dict`/prvek v `set`, což vyžaduje
hashovatelnost. Tahle kontrola proběhne dřív, než se vůbec začne
cokoliv kompilovat.

**Dvoufázová konstrukce (kroky 5 vs. 6–7)** je klíčový architektonický
princip: napřed se **jednou** zkompiluje runtime třída (drahá operace —
sestavení `class_dict`, validace mixinů...), teprve pak se z ní alokuje
instance (levná operace — `object.__new__` + `__init__`). Kdyby šlo o
opakované vytváření instancí se **stejnou** kombinací `mixins`/`mutable`,
kompilace třídy by se dala v budoucnu cachovat na úrovni volajícího kódu.

[▲ Nahoru](#-obsah)

---

## `get_base_class` — výběr strukturálního základu

**Parametry:** `cls`, `is_atom`, `mutable`.

**Návratová hodnota:** jedna ze čtyř již zkompilovaných tříd z metadat.

```python
def get_base_class(cls, is_atom, mutable):
    if is_atom:
        return cls.meta.atom_class_mutable if mutable else cls.meta.atom_class_immutable
    return cls.meta.composite_class_mutable if mutable else cls.meta.composite_class_immutable
```

Čistě směrovací brána přes dvě nezávislé osy — **topologie** (atom vs.
kompozice) a **mutabilita** (mutable vs. immutable). Veškerá složitost
(líné vytváření, cachování) je delegovaná do metadat — tahle funkce sama
o sobě nic nekompiluje, jen vybírá.

[▲ Nahoru](#-obsah)

---

## `create_instance_class` — kompilace finální třídy

**Parametry:** `cls`, `mixins`, `base_class`, `is_atom`, `mutable`.

**Návratová hodnota:** zkompilovaná runtime třída, připravená k alokaci instance.

**Pod kapotou:**
```python
def create_instance_class(cls, mixins, base_class, is_atom, mutable):
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = _build_instance_class_dict(cls, mixins, is_atom, mutable)

    _instance_cls = type(class_name, (base_class,), class_dict)
    _instance_cls.__qualname__ = class_name

    _extend_instance_class(class_dict["__mixins__"], _instance_cls)

    return _instance_cls
```

**Klíčové architektonické rozhodnutí: `(base_class,)` — jediný rodič.**
Mixiny se **nedávají** do `class_parents`, jak by se dalo čekat u
klasického multiple inheritance vzoru. Místo toho jsou zploštěné,
zvalidované a vmíchané přímo do `class_dict` (viz
`_build_instance_class_dict` níže) — tzv. **Namespace Injection Pattern**.

**Proč ne standardní multiple inheritance?** Tři důvody, přímo
z `_DESIGN_NOTES`:

1. **Konflikty rozvržení slotů.** Python nedovolí kombinovat víc tříd s
   neprázdnými `__slots__` v běžné vícenásobné dědičnosti (`TypeError`).
   Injektování slotů mixinů přímo do `class_dict` tenhle limit úplně
   obchází.
2. **Explicitní evidence členství.** Které mixiny instance má, se
   netestuje přes MRO, ale přes explicitní `class_dict["__mixins__"]`
   (tuple zploštěných mixin tříd) — `isinstance(obj, Mixin)` pak funguje
   spolehlivě přes vlastní `__instancecheck__` na `SimpleMixinMeta`, bez
   ohledu na MRO komplikace.
3. **Předvídatelné řešení konfliktů.** Kolize atributů se řeší
   deterministicky už při sestavování `class_dict` (viz níže), ne
   spoléháním na složité MRO pořadí.

[▲ Nahoru](#-obsah)

---

## `_resolve_flat_mixins` — zploštění hierarchie mixinů

**Parametry:** `cls`, `mixins`, `is_atom`, `mutable`.

**Návratová hodnota:** `tuple` — zploštěný, deduplikovaný seznam všech
mixinů (včetně jejich celé MRO ancestry), v pořadí zachovávajícím vložení.

**Pod kapotou (princip):**
```python
def _resolve_flat_mixins(cls, mixins, is_atom, mutable):
    flat_mixins = {}  # dict jako O(1) insertion-ordered set

    for mixin in mixins:
        for mro_mixin in mixin.__mro__:
            if mro_mixin not in (object, SimpleMixin):
                if mro_mixin not in flat_mixins:
                    _verify_mixin_compatibility(cls, mro_mixin, is_atom, mutable)
                    flat_mixins[mro_mixin] = True

    return tuple(flat_mixins.keys())
```

**Proč projíždět celé `__mro__` každého mixinu, ne jen mixin samotný?**
Protože uživatel může předat mixin, který sám dědí z jiných mixinů — funkce
"rozbalí" celý jeho dědičný strom, aby se do finální instance dostalo
kompletně vše, co mixin (a jeho předci) definují.

**`dict` jako množina se zachovaným pořadím vložení** — `mro_mixin not in
flat_mixins` je O(1) kontrola, ale narozdíl od `set` si `dict` (od Pythonu
3.7) pamatuje pořadí, ve kterém byly klíče vloženy. Tohle pořadí je
důležité — `_build_instance_class_dict` ho později prochází **obráceně**,
aby platilo přirozené pravidlo "první v uživatelem zadaném tuple vyhrává"
(viz níže).

**Validace proběhne "za letu"** (`_verify_mixin_compatibility` se volá
hned při objevení nového mixinu, ne až po zploštění celého seznamu) —
takže i nekompatibilní mixin skrytý hluboko v cizí MRO ancestry se odhalí
hned, dřív než se vůbec začne sestavovat finální třída.

[▲ Nahoru](#-obsah)

---

## `_verify_mixin_compatibility` — kompatibilní matice

**Parametry:** `cls`, `mixin`, `is_atom`, `mutable` (výchozí `True`).

**Návratová hodnota:** `None` (vyhazuje výjimku při nekompatibilitě).

**Pod kapotou:**
```python
def _verify_mixin_compatibility(cls, mixin, is_atom, mutable=True):
    if not isinstance(mixin, type) or not issubclass(mixin, SimpleMixin):
        validate_mixin_is_class(cls, mixin)
        validate_mixin_is_simple_base_subclass(cls, mixin)

    if mixin._constant_only and not is_atom:
        raise_mixin_not_allowed_for_composite(cls, mixin)
    if mixin._composite_only and is_atom:
        raise_mixin_not_allowed_for_constant(cls, mixin)
    if mixin._mutable_only and not mutable:
        raise_mixin_not_allowed_for_immutable(cls, mixin)
    if mixin._immutable_only and mutable:
        raise_mixin_not_allowed_for_mutable(cls, mixin)
    if mixin._only_types is not UNSET and not isinstance(cls.meta.default, mixin._only_types):
        raise_mixin_not_support_default_value_type(cls, mixin)
```

Pět nezávislých kontrol, každý mixin deklaruje svoje omezení přes
příznaky (`_constant_only`, `_composite_only`, `_mutable_only`,
`_immutable_only`, `_only_types`) — přesně ty, které jsi zmiňoval v historii
knihovny jako "mixin compatibility flags". Tahle funkce je místo, kde se
ty příznaky **reálně vynucují**, při každém vytváření instance s daným
mixinem.

Poslední kontrola (`_only_types`) je typová — pokud mixin dává smysl jen
pro určité datové typy (např. numerické mixiny jako `Stepper`/`Volume`
z historie knihovny), ověří se, že `cls.meta.default` je instancí
očekávaného typu, dřív než se mixin vůbec připojí.

[▲ Nahoru](#-obsah)

---

## `_build_instance_class_dict` — namespace injection

**Parametry:** `cls`, `mixins`, `is_atom`, `mutable`.

**Návratová hodnota:** kompletní `class_dict`, připravený pro `type(...)`.

**Sedm kroků:**

1. **Zploštění mixinů** přes `_resolve_flat_mixins`.
2. **Základní namespace** — `__is_constant__`, `__is_mutable__`, `__mixins__`.
3. **Příprava akumulátorů** — `init_mixins` (list hooků), `mixin_slots`
   (dict), a `class_slots` — množina všech slotů zděděných z `cls.__mro__`
   (tedy ze strukturálního základu, atomu/kompozice).
4. **Iterace mixinů v obráceném pořadí** (`reversed(all_unique_mixins)`) —
   tohle je jádro mechanismu přepisování atributů.
5. Pro každý mixin: kontrola kolize slotů (proti base class i proti dřív
   zpracovaným mixinům) a extrakce namespace (metody, atributy).
6. Sloučení sesbíraných `init_mixins` hooků do jednoho (viz níže).
7. Finalizace `__slots__` z `mixin_slots`.

**Proč `reversed(...)`?** Tohle je klíčový detail pro pochopení priority
mixinů. Uživatel zadává `mixins=(MixinA, MixinB)` s očekáváním, že
`MixinA` (napsaný **první**) má přednost, pokud oba definují stejný
atribut. Ale `class_dict[key] = value` v cyklu **přepisuje** předchozí
hodnotu — takže aby `MixinA` "vyhrál", musí se zpracovat **jako poslední**.
Iterace v obráceném pořadí přesně tohle zařizuje.

**Kolize slotů jsou fatální, ne tiše přepsané.** Narozdíl od běžných
atributů/metod (kde přepsání je záměrné a v pořádku), kolize **jména
slotu** je vždy chyba — buď proti základní strukturální třídě
(`raise_mixin_slot_collision_with_base_class`), nebo mezi dvěma mixiny
navzájem (`raise_mixin_slot_collision`). Dva mixiny se stejným slotem by
si navzájem přepisovaly paměťové místo — to by byl těžko odhalitelný,
tichý bug, proto se to řeší jako tvrdá chyba hned při kompilaci.

**`IGNORED_DICT_KEYS`** — sada klíčů, které se z namespace mixinu nikdy
nekopírují (`__dict__`, `__weakref__`, `__slots__` samo o sobě, `__doc__`,
`__module__`, `__init_subclass__`, `__extend_instance_class__`). Buď jde o
framework "boilerplate", který by znečistil cílovou třídu, nebo (u
`__extend_instance_class__`) o hook, který se zpracovává samostatně, **po**
kompilaci třídy (viz `_extend_instance_class` níže).

**`init_mixins` se nekopíruje jako obyčejný atribut** — pokud klíč je
přesně `"init_mixins"`, funkce se místo přímého zápisu do `class_dict`
přidá do seznamu `init_mixins` (kroku 3), aby ji `_build_combined_init_mixins`
mohla zřetězit se všemi ostatními.

[▲ Nahoru](#-obsah)

---

## `_build_combined_init_mixins` — řetězení inicializace

**Parametry:** `init_mixins_hooks` (list funkcí).

**Návratová hodnota:** jedna sloučená funkce `combined_init_mixins`.

**Pod kapotou:**
```python
def _build_combined_init_mixins(init_mixins_hooks):
    def combined_init_mixins(self):
        for init_mixin in init_mixins_hooks:
            init_mixin(self)
    return combined_init_mixins
```

Triviální na pohled, ale architektonicky důležité: místo řetězu
`super().init_mixins()` volání (což by v dynamicky skládané hierarchii
znamenalo spoléhat na MRO) se všechny nasbírané `init_mixins` hooky
zavolají **explicitně a sekvenčně** v jedné uzavřené funkci. Stejný
princip jako "bez `super()`" u `create_composite_init` (viz
[README_COMPOSITE_CLASS.md](README_COMPOSITE_CLASS.md#create_composite_init--konstruktor)) —
konzistentní preference explicitního, deterministického pořadí před
implicitním MRO řešením.

[▲ Nahoru](#-obsah)

---

## `_extend_instance_class` — post-kompilační hooky

**Parametry:** `mixins` (zploštěný tuple), `instance_class` (už
zkompilovaná třída).

**Návratová hodnota:** `None` — mutuje `instance_class` **na místě**.

**Pod kapotou:**
```python
def _extend_instance_class(mixins, instance_class):
    for mixin in mixins:
        if "__extend_instance_class__" in mixin.__dict__:
            raw_attr = mixin.__dict__["__extend_instance_class__"]
            if not isinstance(raw_attr, (staticmethod, classmethod)):
                raise_invalide_extend_instance_class_definition(instance_class, mixin)
            mixin.__extend_instance_class__(instance_class)
```

Tenhle hook je **únikový ventil** pro mixiny, které potřebují víc než jen
statický `class_dict` merge — typicky mixiny jako `InnersProperty` nebo
`Equalizer`, které musí dynamicky generovat properties/settery **až po
tom**, co je finální třída hotová (protože třeba potřebují znát kompletní
`__mixins__` sadu, nebo jiné informace dostupné až na zkompilované
třídě).

**Přímá kontrola `mixin.__dict__`, ne `getattr`** — záměrně se čte přímo ze
slovníku třídy, aby se předešlo předčasnému vyhodnocení deskriptoru
(`getattr` by mohl spustit `__get__` a nechtěně zavolat metodu).

**Vynucený `@staticmethod`/`@classmethod`.** Obyčejná instanční metoda by
tu nedávala smysl — hook se volá na úrovni **třídy**, ne instance
(instance ještě ani neexistuje, jen kompilovaná třída).

**Vrací `None`, mutuje na místě** — stejná konvence jako `list.sort()`
v Pythonu: signalizuje, že `instance_class` byla změněna přímo v paměti,
ne že se vrací nová třída.

[▲ Nahoru](#-obsah)
