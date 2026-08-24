# ⚙️ Zpracování classmethod — `_validate`, `_logic`, `_decompose`

Tenhle dokument popisuje **jednu sdílenou pipeline**, kterou prochází
všechny tři uživatelsky definovatelné classmethody v systému: `_validate`
(na `SimpleConstant` i `SimpleObject`), `_logic` a `_decompose` (obě jen na
`SimpleObject`). Místo aby měl každý typ metody vlastní, duplicitní
ověřovací logiku, volají `SimpleConstantMetadata` i `SimpleObjectMetadata`
stejnou vstupní funkci — `process_classmethod` — jen s jinými parametry.

➡️ Používá se z: [README_SIMPLE_CONSTANT_METADATA.md](README_SIMPLE_CONSTANT_METADATA.md),
[README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md)

---

## 🧭 Obsah

* [Přehled pipeline](#přehled-pipeline)
* [`process_classmethod` — vstupní bod](#process_classmethod--vstupní-bod)
* [`verify_classmethod` — brána: validovat, klonovat, nebo zdědit?](#verify_classmethod--brána-validovat-klonovat-nebo-zdědit)
* [`_clone_classmethod` — izolace zděděných metod](#_clone_classmethod--izolace-zděděných-metod)
* [`verify_params` — kontrola signatury na úrovni bytecode](#verify_params--kontrola-signatury-na-úrovni-bytecode)
* [`verify_annotations_and_defaults` — kontrola volitelných anotací](#verify_annotations_and_defaults--kontrola-volitelných-anotací)
* [`verify_calculation` — dry-run a kontrola výsledku](#verify_calculation--dry-run-a-kontrola-výsledku)
* [`verify_decompose_outcome` — speciální pravidla pro `_decompose`](#verify_decompose_outcome--speciální-pravidla-pro-_decompose)

---

## Přehled pipeline

```
process_classmethod
│
├─ 1. verify_classmethod  ──────► rozhodne: validovat? klonovat? přeskočit?
│
├─ 2. (pokud need_validations)
│     ├─ verify_params
│     └─ verify_annotations_and_defaults  (jen pokud uživatel něco deklaroval)
│
├─ 3. injektuje normalizované defaulty/anotace do __func__
│
└─ 4. verify_calculation ──────► dry-run + kontrola typu výsledku
      └─ (jen pro _decompose) verify_decompose_outcome
```

Celá pipeline běží **jednou, při definici třídy** — ne při každém volání
metody za běhu. Výsledkem je buď zvalidovaná, doplněná classmethod (a
u `_logic` i rovnou spočítaný default), nebo `UNSET`, pokud metoda nebyla
definovaná a je volitelná.

[▲ Nahoru](#-obsah)

---

## `process_classmethod` — vstupní bod

**Parametry:**
* `method_name` (*str*): `"_validate"`, `"_logic"` nebo `"_decompose"`.
* `expected_params`, `expected_args_params_count`: očekávaná signatura.
* `expected_args_defaults`, `expected_kwargs_defaults`: očekávané defaulty.
* `expected_param_types`, `expected_return_type`: očekávané anotace.
* `owner_class`: třída, na které se metoda zpracovává.
* `test_value` (*tuple*, výchozí `()`): argumenty pro dry-run.
* `return_calculated_value` (*bool*, výchozí `False`): pokud `True`, vrátí
  dvojici `(metoda, spočítaná_hodnota)` místo jen metody — používá se pro
  `_logic`, kde je výsledek dry-runu zároveň výchozí hodnotou kompozice.

**Návratová hodnota:**
* `ClassMethodProtocol` (validovaná metoda), nebo `(metoda, hodnota)`
  pokud `return_calculated_value=True`, nebo `UNSET`/`(UNSET, UNSET)`,
  pokud je metoda volitelná a chybí.

**Pod kapotou (zkráceně):**
```python
def process_classmethod(method_name, expected_params, ..., owner_class,
                         test_value=(), return_calculated_value=False):
    need_validations, bound_method = verify_classmethod(...)

    if bound_method is UNSET:
        return (UNSET, UNSET) if return_calculated_value else UNSET

    if need_validations:
        verify_params(...)
        bound_method_annotations = {**expected_param_types, "return": expected_return_type}
        if func.__annotations__ or func.__defaults__ or func.__kwdefaults__:
            verify_annotations_and_defaults(...)
        func.__defaults__ = expected_args_defaults
        func.__kwdefaults__ = expected_kwargs_defaults
        func.__annotations__ = bound_method_annotations

    calculated_value = verify_calculation(bound_method, test_value, expected_return_type, owner_class)

    return (bound_method, calculated_value) if return_calculated_value else bound_method
```

Klíčový detail: **anotace a defaulty se do funkce injektují natvrdo**
(`func.__defaults__ = ...`), i když je uživatel vůbec nenapsal. Metoda tak
po zpracování vždy vypadá navenek stejně — s kompletní, konzistentní
signaturou — bez ohledu na to, jak stručně ji uživatel napsal.

[▲ Nahoru](#-obsah)

---

## `verify_classmethod` — brána: validovat, klonovat, nebo zdědit?

Tohle je centrální rozhodovací bod celé pipeline — určuje, jestli se metoda
vůbec musí znovu validovat, nebo jestli může (bezpečně) zůstat, jak je
zděděná z rodiče.

**Parametry:** `method_name`, `owner_class`, `expected_params`, `expected_args_params_count`

**Návratová hodnota:**
* `tuple[bool, classmethod | UNSET]` — `(need_validations, bound_method)`.

**Rozhodovací strom (zjednodušeně):**

1. **Speciální zkratka pro nedefinovaný `_decompose`.** Pokud metoda
   `_decompose` není lokálně přepsaná (`raw_method is UNSET`) a zděděná
   verze ukazuje přesně na `SimpleObject._decompose` (kontrola identity
   přes `is` na `__func__`, tedy porovnání paměťové adresy, ne obsahu) →
   vrací se rovnou `(False, UNSET)`. Tohle zabraňuje zbytečnému
   spouštění dry-runu pro metodu, která je stále jen defaultní
   "nedekomponovatelná" implementace.
2. **Lokální přepsání (`raw_method is not UNSET`)** → vždy `(True,
   bound_method)`. Cokoliv, co uživatel napsal přímo na téhle třídě, se
   musí ověřit od nuly.
3. **Zděděné `_validate`** → vždy `(False, bound_method)`. Validační
   pravidla patří třídě, která je definovala — zděděná `_validate` se
   nikdy znovu neověřuje.
4. **Hluboké zanoření (třída není přímý potomek `SimpleObject`)** → pokud
   podtřída mění strukturální klíče (`_inners`, `_type`, `_logic`), zděděná
   metoda se **naklonuje** přes `_clone_classmethod`, aby injekce
   nových metadat (krok 3 v `process_classmethod`) neovlivnila původní
   funkční objekt sdílený s rodičovskou třídou.
5. **Nic z výše uvedeného nesedí** → metoda je strukturálně vadná (není
   `classmethod`, není definovaná, atd.) → spustí se sada
   mikro-validátorů (`validate_method_is_defined`,
   `validate_method_is_callable`, `validate_method_is_classmethod`), které
   vyprodukují přesnou chybovou hlášku.

**Proč je krok 4 důležitý:** `classmethod` v Pythonu obaluje jeden sdílený
funkční objekt. Kdyby se do zděděné metody injektovaly nové defaulty/anotace
přímo (bez klonování), propsalo by se to zpětně i do rodičovské třídy —
tichá, těžko odhalitelná chyba sdíleného stavu. Klonování tomuhle
předchází tím, že hluboce zanořené podtřídy dostanou vlastní, nezávislou
kopii.

[▲ Nahoru](#-obsah)

---

## `_clone_classmethod` — izolace zděděných metod

**Parametry:** `cm` (*classmethod*) — metoda ke klonování.

**Návratová hodnota:** nový, plně nezávislý `classmethod` objekt.

**Pod kapotou:**
```python
def _clone_classmethod(cm):
    func = cm.__func__
    new_func = FunctionType(
        func.__code__, func.__globals__, name=func.__name__,
        argdefs=func.__defaults__, closure=func.__closure__,
    )
    new_func.__annotations__ = dict(func.__annotations__)
    new_func.__kwdefaults__ = dict(func.__kwdefaults__) if func.__kwdefaults__ else None
    if func.__dict__:
        new_func.__dict__.update(func.__dict__)
    return classmethod(new_func)
```

Znovu-sestaví kompletně nový `FunctionType` ze stejného bytecode
(`__code__`), stejných globálů a closure, ale s **vlastními** kopiemi
anotací, defaultů a atributů. Tenhle nový funkční objekt už je bezpečné
mutovat (přes `func.__defaults__ = ...` v `process_classmethod`), aniž by
to ovlivnilo originál.

[▲ Nahoru](#-obsah)

---

## `verify_params` — kontrola signatury na úrovni bytecode

**Parametry:** `expected_params`, `expected_args_params_count`, `bound_method`

**Návratová hodnota:** `None` (vyhazuje výjimku při neshodě).

**Proč bytecode, ne `inspect`:** funkce čte signaturu přímo z
`__code__` (`co_argcount`, `co_kwonlyargcount`, `co_varnames`,
`co_flags`) místo přes modul `inspect`. Je to rychlejší a pro tenhle účel
plně dostatečné — potřebujeme jen jména parametrů, jejich počet a
přítomnost `*args`/`**kwargs`.

**Šťastná cesta (short-circuit):** pokud metoda nemá `*args` ani
`**kwargs`, počet pozičních parametrů sedí a jména parametrů sedí přesně
(`method_params == expected_params`), funkce se okamžitě vrátí — žádné
další zpracování. Teprve když něco nesedí, sestaví se `exception_info`
a `expected_structure` (čitelný "blueprint" správné signatury) a spustí se
tři mikro-validátory, které přesně určí, co je špatně: špatná jména/pořadí
parametrů, špatný počet argumentů, nebo použití `*args`/`**kwargs` (které
jsou pro `_validate`/`_logic`/`_decompose` zakázané — signatura musí být
plně explicitní).

[▲ Nahoru](#-obsah)

---

## `verify_annotations_and_defaults` — kontrola volitelných anotací

Spouští se jen tehdy, když uživatel **sám** něco deklaroval (anotace typu
nebo defaultní hodnoty) — jinak se přeskočí, protože `process_classmethod`
stejně vše na konci injektuje automaticky.

**Parametry:** `bound_method`, `expected_params`, `expected_args_params_count`,
`bound_method_annotations`, `expected_args_defaults`, `expected_kwargs_defaults`

**Návratová hodnota:** `None` (vyhazuje výjimku při neshodě).

**Pravidlo:** *anotace a defaulty smí chybět, ale pokud jsou přítomné,
musí přesně odpovídat tomu, co systém očekává.* To znamená tři nezávislé
kontroly, každá spuštěná jen pokud je relevantní část přítomná:

* `func.__annotations__` → `validate_annotations` (anotace musí být
  podmnožinou očekávaných typů),
* `func.__defaults__` → `validate_args_defaults` (poziční defaulty musí
  odpovídat defaultům odvozeným z `_inners`),
* `func.__kwdefaults__` → `validate_kwargs_defaults`.

Tenhle přístup dává uživateli svobodu — může (ale nemusí) psát typové
anotace pro vlastní čitelnost/IDE support — ale pokud je napíše špatně,
systém to okamžitě odhalí při definici třídy, ne až za běhu.

[▲ Nahoru](#-obsah)

---

## `verify_calculation` — dry-run a kontrola výsledku

Poslední a nejdůležitější krok: metoda se **skutečně spustí** (s testovacími
hodnotami) už při definici třídy, ne až při prvním použití.

**Parametry:** `bound_method`, `test_value`, `expected_return_type`, `owner_class`

**Návratová hodnota:** `Any` — výsledek dry-runu (nebo `UNSET`, pokud
`bound_method` je `UNSET`).

**Pod kapotou:**
```python
def verify_calculation(bound_method, test_value, expected_return_type, owner_class):
    if bound_method is UNSET:
        return UNSET

    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        raise_method_raised_exceptions(e, bound_method)

    if not isinstance(calculate_result, expected_return_type):
        raise_method_return_unvalide_outcome_type(calculate_result, expected_return_type, bound_method)

    if bound_method.__func__.__name__ == "_decompose":
        verify_decompose_outcome(calculate_result, owner_class, bound_method)

    return calculate_result
```

**Proč dry-run už při definici třídy:** tohle je jeden z klíčových
architektonických principů celého systému — chyby v uživatelské logice
(`_logic` vrací špatný typ, `_validate` vyhazuje neočekávanou výjimku,
`_decompose` vrací tuple špatné délky) se odhalí **okamžitě při importu
modulu**, ne až v produkci při první reálné instanci. Testovací hodnoty
(`test_value`) jsou přitom vždy odvozené z defaultů — takže dry-run běží
nad hodnotami, o kterých už systém ví, že jsou platné.

U `_logic` je tenhle dry-run navíc přímo **zdrojem výchozí hodnoty celé
kompozice** — `process_classmethod` s `return_calculated_value=True` vrátí
`calculated_value` z `verify_calculation` a `SimpleObjectMetadata` ji rovnou
použije jako `self.default`. Jinými slovy: `_default` kompozice není nic
jiného než výsledek jejího vlastního dry-runu.

[▲ Nahoru](#-obsah)

---

## `verify_decompose_outcome` — speciální pravidla pro `_decompose`

Spouští se jen tehdy, když ověřovaná metoda je `_decompose` — kontroluje,
že vrácený tuple strukturálně odpovídá `_inners`.

**Parametry:** `calculate_default` (výsledek dry-runu), `owner_class`, `bound_method`

**Návratová hodnota:** `None` (vyhazuje výjimku při neshodě).

**Dvě úrovně kontroly:**

1. **Délka.** Vrácený tuple musí mít přesně tolik prvků, kolik má
   `_inners` — jinak `raise_decompose_unvalide_outcome_length`.
2. **Jednotlivé položky.** Pro každou pozici se kontroluje, jestli hodnota
   buď odpovídá typu daného vnitřního prvku (`isinstance(value,
   expected_type)`), nebo se rovná jeho defaultu (`value ==
   inner.meta.default`) — druhá podmínka je záměrná úleva pro dry-run
   scénář, kdy dekompozice defaultní hodnoty kompozice přirozeně vrací
   defaulty jednotlivých `_inners`, které nemusí být striktně
   `isinstance`-kompatibilní (např. sentinely). Pokud neplatí ani jedno,
   spustí se mikro-validátory pro přesnou diagnostiku.

[▲ Nahoru](#-obsah)
