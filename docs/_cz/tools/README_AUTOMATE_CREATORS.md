# 🏭 Automate Creators — Programové vytváření tříd bez `class` zápisu

Standardní způsob definice v Simple systému je psát `class MyConstant(SimpleConstant): ...`
napevno v kódu. Tenhle nástroj dává alternativu: **vytvořit blueprint
třídy programově, za běhu**, z hodnot, které třeba přišly z konfigurace,
databáze, nebo uživatelského vstupu. Tři veřejné funkce tvoří jasnou
hierarchii:

```
create_simple_object          (univerzální fasáda — rozhoduje atom vs. kompozice)
├── create_constant_class      (staví SimpleConstant podtřídy)
└── create_object_class        (staví SimpleObject podtřídy)
```

---

## 🧭 Obsah

* [`create_constant_class` — programová konstanta](#create_constant_class--programová-konstanta)
* [`create_object_class` — programová kompozice](#create_object_class--programová-kompozice)
* [`create_simple_object` — univerzální fasáda](#create_simple_object--univerzální-fasáda)
* [Pomocné funkce](#pomocné-funkce)
  * [`_is_lambda`](#_is_lambda)
  * [`process_validate` a `process_decompose`](#process_validate-a-process_decompose)
  * [`process_logic`](#process_logic)
  * [`load_parameters_from_inners`](#load_parameters_from_inners)
  * [`calculate_default`](#calculate_default)

---

## `create_constant_class` — programová konstanta

**Parametry:**
* `class_name` (*str*): jméno nové třídy.
* `default` (*Any*): povinná výchozí hodnota.
* `value_type` (*type | UNSET*): explicitní typ; pokud `UNSET`, odvodí se z `type(default)`.
* `validate` (*Callable | UNSET*): volitelná validační funkce nebo lambda.

**Návratová hodnota:** nová `SimpleConstant` podtřída (blueprint, ne instance).

**Pod kapotou (zkráceně):**
```python
def create_constant_class(class_name, default, value_type=UNSET, validate=UNSET):
    ...
    if value_type is UNSET:
        value_type = type(default)

    namespace = {"_default": default, "_type": value_type}

    if validate is not UNSET:
        namespace["_validate"] = classmethod(process_validate(validate))

    return type(class_name, (SimpleConstant,), namespace)
```

**Odvození typu z hodnoty je pohodlný default, ne magie.** Pokud uživatel
nezadá `value_type` explicitně, systém prostě zavolá `type(default)` —
stejně, jako by to typicky napsal ručně (`_type = int` pro `_default =
20`). Tohle šetří psaní v jednoduchých případech, ale zůstává plně
přepsatelné, když je potřeba typ volnější (např. union).

Funkce je tenký obal nad tím, co by jinak vyžadovalo napsat celou `class`
definici — výsledek prochází přesně stejnou `SimpleMeta`/`SimpleConstantMetadata`
pipeline jako ručně psaná třída (viz
[README_SIMPLE_META.md](README_SIMPLE_META.md#__new__--vznik-třídy)),
protože `type(class_name, (SimpleConstant,), namespace)` spouští úplně
stejný mechanismus jako `class` klíčové slovo v Pythonu.

[▲ Nahoru](#-obsah)

---

## `create_object_class` — programová kompozice

**Parametry:**
* `class_name` (*str*): jméno nové třídy.
* `inners` (*tuple*): vnitřní prvky.
* `logic` (*Callable*): povinná výpočetní funkce.
* `value_type` (*type | UNSET*): explicitní typ; pokud `UNSET`, odvodí se z dry-runu `logic`.
* `validate`, `decompose` (*Callable | UNSET*): volitelné hooky.

**Návratová hodnota:** nová `SimpleObject` podtřída.

**Pod kapotou (zkráceně):**
```python
def create_object_class(class_name, inners, logic, value_type=UNSET, validate=UNSET, decompose=UNSET):
    ...
    _params = load_parameters_from_inners(class_name, inners)
    _logic = process_logic(logic, _params.keys())

    if value_type is UNSET:
        _default_value = calculate_default(_logic, tuple(_params.values()))
        value_type = type(_default_value)

    namespace = {"_inners": inners, "_type": value_type, "_logic": classmethod(_logic)}
    ...
    return type(class_name, (SimpleObject,), namespace)
```

**Odvození typu je tu o krok složitější než u konstanty** — nestačí
`type(default)`, protože kompozice žádný explicitní default nemá (viz
[README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#důležité-_default-se-nesmí-definovat)).
Místo toho se `logic` **skutečně jednou zavolá** s výchozími hodnotami
odvozenými z `inners` (`calculate_default`, viz níže) a typ výsledku se
použije jako `value_type`. Je to menší, ruční předehra k tomu, co pak
stejně dělá `SimpleObjectMetadata` (dry-run `_logic` — viz
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md#verify_calculation--dry-run-a-kontrola-výsledku)) —
tady se to jen musí udělat o krok dřív, protože `value_type` je potřeba
znát **předtím**, než se sestaví `namespace` pro `type(...)`.

**`logic` prochází normalizací signatury** (`process_logic`) předtím, než
se z ní vůbec zkusí spočítat default — to řeší nejčastější zdroj tření
u programového API: uživatel typicky nechce psát `lambda cls, a, b: ...`,
chce jen `lambda a, b: ...` (viz [pomocné funkce](#process_logic) níže).

[▲ Nahoru](#-obsah)

---

## `create_simple_object` — univerzální fasáda

**Parametry:** sjednocuje parametry obou tvůrců plus:
* `return_instance` (*bool*, výchozí `False`): pokud `True`, vrátí rovnou
  instanci místo blueprintu.
* `mixins`, `as_atom`, `mutable`: předávané do `SimpleMeta.__call__`, pokud
  `return_instance=True`.

**Návratová hodnota:** buď blueprint třída, nebo instance (podle `return_instance`).

**Pod kapotou:**
```python
def create_simple_object(class_name, default=UNSET, inners=UNSET, ..., return_instance=False, ...):
    if inners is UNSET:
        _class = create_constant_class(class_name=class_name, default=default, ...)
    else:
        _class = create_object_class(class_name=class_name, inners=inners, ...)

    return _class if not return_instance else _class(mixins=mixins, as_atom=as_atom, mutable=mutable)
```

**Směrovací pravidlo je jediný `if inners is UNSET`** — stejný princip
jako u `SimpleMeta.__new__`, kde přítomnost `_inners` rozlišuje konstantu
od kompozice (viz
[README_SIMPLE_META.md](README_SIMPLE_META.md#__new__--vznik-třídy)).
Tady se to samé rozhodnutí dělá ještě před vytvořením třídy, ne až uvnitř
metaclassy — protože `create_constant_class` a `create_object_class` mají
each odlišnou sadu povinných parametrů (default vs. inners+logic).

**`create_simple_object` je jediné veřejné API, které dovede vrátit rovnou
hotovou instanci** (`return_instance=True`) — poslední řádek jen deleguje
na `_class(...)`, což je přesně to volání, které spustí `SimpleMeta.__call__`
→ `create_instance` (viz [README_CREATE_INSTANCE.md](README_CREATE_INSTANCE.md)).
Tohle je typický vzor "vytvoř třídu i instanci v jednom kroku", vhodný pro
scénáře, kde blueprint stejně nikdo nebude znovu používat (např.
jednorázová konstanta z konfiguračního souboru).

[▲ Nahoru](#-obsah)

---

## Pomocné funkce

### `_is_lambda`

```python
def _is_lambda(fn):
    return callable(fn) and getattr(fn, "__name__", None) == "<lambda>"
```

Malý, ale klíčový detekční nástroj — všechny tři `process_*` funkce níže
se chovají jinak podle toho, jestli dostaly pojmenovanou funkci, nebo
anonymní `lambda`. Detekce je jednoduchá: každá `lambda` v Pythonu má
`__name__ == "<lambda>"`, bez ohledu na to, do jaké proměnné je přiřazená.

[▲ Nahoru](#-obsah)

---

### `process_validate` a `process_decompose`

Obě fungují na stejném principu — normalizují **signaturu** uživatelské
funkce, ne její chování:

```python
def process_validate(validate):
    if not _is_lambda(validate):
        return validate

    def _validate(cls, value, *, return_bool=False):
        return validate(value)

    return _validate
```

```python
def process_decompose(decompose):
    if not _is_lambda(decompose):
        return decompose

    def _decompose(cls, value):
        return decompose(value)

    return _decompose
```

**Proč tohle vůbec existuje:** systém interně vždy volá `_validate(cls,
value, *, return_bool=...)` a `_decompose(cls, value)` — signatury pevně
dané a ověřované přes `verify_params` (viz
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md#verify_params--kontrola-signatury-na-úrovni-bytecode)).
Ale když uživatel v programovém API napíše `lambda v: v > 0`, chybí mu
`cls` (a u validate i `return_bool`) — a lambda navíc nejde snadno
"rozšířit" o další parametr bez přepsání. Obě funkce tedy pojmenovanou
funkci nechají beze změny (předpokládá se, že už má správnou signaturu),
ale lambdu **obalí** do wrapperu se správnou signaturou, který uvnitř
zavolá původní lambdu jen s tím, co skutečně potřebuje (`value`).

**Asymetrie mezi funkcemi a `process_logic`** (viz níže) není náhoda —
`process_validate`/`process_decompose` mají vždy stejný, pevný počet
parametrů (`value`, případně `return_bool`), takže obyčejný `def` wrapper
stačí. `process_logic` na tenhle trik nemůže spoléhat, protože počet
parametrů `_logic` je proměnlivý (podle počtu `_inners`) — proto potřebuje
jiný přístup.

[▲ Nahoru](#-obsah)

---

### `process_logic`

```python
def process_logic(logic, params_name):
    if not _is_lambda(logic):
        return logic

    params = ", ".join(params_name)
    src = f"def _logic(cls, {params}): return logic({params})"

    namespace = {"logic": logic}
    exec(src, namespace)

    return namespace["_logic"]
```

Tady obyčejný pevný wrapper nestačí — `_logic` musí mít **přesně tolik
parametrů, kolik má kompozice `_inners`**, a to číslo je předem neznámé
(je to `params_name`, odvozené z konkrétní kompozice). Řešení je sestavit
zdrojový kód wrapperu **jako řetězec** a zkompilovat ho přes `exec` — pro
`_inners = (Width, Height)` by to vygenerovalo přesně:

```python
def _logic(cls, width, height): return logic(width, height)
```

Tohle je jedno z mála míst v celé knihovně, kde se používá `exec` — a je
to záměrně izolované právě sem, protože jde o jediný praktický způsob, jak
vyrobit funkci s **dynamickým počtem pojmenovaných parametrů** (na rozdíl
od `*args`, které by ale nevyhovovalo přísné kontrole signatury v
`verify_params`).

[▲ Nahoru](#-obsah)

---

### `load_parameters_from_inners`

**Parametry:** `class_name` (pro diagnostiku), `inners` (tuple blueprintů).

**Návratová hodnota:** `dict[str, Any]` — `{name_snake: default}` pro
každý vnitřní prvek.

```python
def load_parameters_from_inners(class_name, inners):
    if not isinstance(inners, tuple):
        raise_inners_is_not_tuple(class_name, inners)

    params = {}
    for inner in inners:
        if not issubclass(inner, SimpleConstant):
            raise_inner_is_not_simple_constant_subclass(class_name, inner)
        params[inner.meta.name_snake] = inner.meta.default

    return params
```

Přímočará extrakce — pro každý `inner` (musí být podtřída `SimpleConstant`,
tedy atom nebo kompozice) se vezme jeho `name_snake` a `default` z už
existujících, hotových metadat. Výsledek slouží dvakrát: jednou jako
zdroj jmen parametrů pro `process_logic`, podruhé jako zdroj hodnot pro
`calculate_default`.

[▲ Nahoru](#-obsah)

---

### `calculate_default`

**Parametry:** `logic` (už normalizovaná, s `cls` parametrem), `params`
(tuple hodnot v pořadí `inners`).

**Návratová hodnota:** vypočítaná výchozí hodnota.

```python
def calculate_default(logic, params):
    try:
        cls = None
        return logic(cls, *params)
    except Exception as exc:
        raise_calculate_default_failed(logic, params, exc)
```

**`cls = None` je vědomý kompromis.** V tomhle bodě ještě **neexistuje**
žádná třída, jejíž metodou by `logic` byla — teprve se buduje `namespace`,
který se za chvíli použije k vytvoření té třídy. `_logic` funkce nicméně
očekává `cls` jako první parametr (kvůli konzistenci s tím, jak `_logic`
vypadá na ručně psaných třídách). Protože typická `_logic` implementace
`cls` stejně nepoužívá (jen čte hodnoty parametrů), předání `None` je
bezpečné a umožňuje to spustit dry-run dřív, než třída vůbec existuje.

[▲ Nahoru](#-obsah)
