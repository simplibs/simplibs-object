# ⚛️ `SimpleConstant` — Deklarativní atom

`SimpleConstant` je základní stavební kámen celého systému — reprezentuje
jednu typovanou hodnotu ("atom"), která umí sama sebe zvalidovat a
normalizovat. Atomy se používají jak samostatně (např. jako typované,
sebe-validující hodnoty v jiné knihovně), tak jako vnitřní prvky (`_inners`)
kompozitních objektů `SimpleObject`.

```
SimpleBase
└── SimpleConstant     ← jsi tady
    └── SimpleObject
```

---

## 🧭 Obsah

* [Deklarativní rozhraní](#deklarativní-rozhraní)
  * [`_type`](#_type)
  * [`_default`](#_default)
  * [`_validate`](#_validate)
* [Veřejné API](#veřejné-api)
  * [`validate_type`](#validate_type)
  * [`validate`](#validate)
  * [`is_valid`](#is_valid)
  * [`normalize`](#normalize)
  * [`bool_or_raise_validate_error`](#bool_or_raise_validate_error)
* [Validační pipeline jako celek](#validační-pipeline-jako-celek)

---

## Deklarativní rozhraní

Tohle je vše, co uživatel při definici konstanty píše sám:

```python
class Age(SimpleConstant):
    _type = int
    _default = 20

    @classmethod
    def _validate(cls, value, *, return_bool=False):
        if value < 0:
            return cls.bool_or_raise_validate_error(
                value, "Věk nemůže být záporný.", return_bool=return_bool
            )
        return True
```

### `_type`

Povinná typová anotace. Metadata (`SimpleConstantMetadata`) ji při definici
třídy zpracují a zpřístupní jako `cls.meta.value_type` — z tohoto místa
vychází veškerá typová validace v systému.

### `_default`

Povinná výchozí hodnota. Musí projít typovou validací proti `_type` už
v okamžiku definice třídy — takže neplatný default se odhalí okamžitě, ne
až za běhu při první instanci.

### `_validate`

Volitelný hook pro rozšířenou validaci nad rámec pouhé kontroly typu. Pokud
ho uživatel nepřepíše, výchozí implementace vrací `True` — tedy "žádná
další pravidla, stačí typová shoda". Metoda může:

* vrátit `True`/`False`,
* vyhodit vlastní výjimku,
* použít pomocnou [`bool_or_raise_validate_error`](#bool_or_raise_validate_error)
  pro strukturované hlášení chyby.

[▲ Nahoru](#-obsah)

---

## Veřejné API

Všechny metody níže jsou na `SimpleConstant` jen tenké wrappery — obsahují
minimum logiky a delegují na interní funkce v
`_core/logic/constant_methods/`. Tenhle vzor (tenký veřejný obal + interní
funkce s `_DESIGN_NOTES`) se opakuje napříč celou knihovnou.

### `validate_type`

Deterministická typová validace, čistě na základě metadat — bez zapojení
uživatelské `_validate` logiky.

**Parametry:**
* `value` (*Any*): hodnota k ověření.
* `return_bool` (*bool*, výchozí `False`): pokud `True`, vrátí `False`
  místo vyhození výjimky.

**Návratová hodnota:**
* `True`, pokud hodnota odpovídá typu.
* `False`, pokud `return_bool=True` a typ nesedí.
* `None`, pokud `return_bool=False` a validace projde (implicitní návrat).

**Výjimky:**
* `SimpleRuntimeError`, pokud `return_bool=False` a typ nesedí.

**Pod kapotou:**
```python
def validate_type(cls, value, *, return_bool=False):
    if isinstance(value, cls.meta.value_type):
        return True
    if return_bool:
        return False
    raise_type_error(cls, value)
```

Celá funkce je záměrně minimální — jediné, co dělá navíc oproti holému
`isinstance`, je rozhodnutí "vrátit bool, nebo vyhodit strukturovanou
chybu". Veškerá diagnostika (co přesně nesedí, jak to opravit) je
delegovaná do `raise_type_error`.

[▲ Nahoru](#-obsah)

---

### `validate`

Spustí kompletní validační pipeline: typová validace **+** uživatelská
`_validate` logika.

**Parametry:**
* `value` (*Any*): hodnota k ověření.
* `return_bool` (*bool*, výchozí `False`).

**Návratová hodnota:**
* `True`/`False`/`None` podle stejné konvence jako `validate_type`.

**Výjimky:**
* `SimpleRuntimeError`, pokud `return_bool=False` a validace selže.

**Pod kapotou:**
```python
def validate(cls, value, *, return_bool=False):
    try:
        result = (
            cls.validate_type(value, return_bool=return_bool)
            and cls.meta.validate(value, return_bool=return_bool)
        )
    except Exception as e:
        if return_bool:
            return False
        if isinstance(e, SimpleObjectError):
            raise
        raise_unexpected_validation_error(cls, value, e)

    if result is False and not return_bool:
        raise_validation_error(cls, value)

    return result
```

Tři věci, které stojí za povšimnutí:

1. **Krátké vyhodnocení (`and`).** Uživatelská `_validate` se vůbec
   nespustí, pokud typová validace selže — nemá smysl validovat hodnotu
   špatného typu proti doménovým pravidlům.
2. **Rozlišení očekávaných a neočekávaných výjimek.** Pokud uživatelská
   `_validate` vyhodí `SimpleObjectError`, je to považováno za "očekávanou"
   strukturovanou chybu a jde dál beze změny. Cokoliv jiného (typicky bug
   v uživatelském kódu) se zabalí přes `raise_unexpected_validation_error`,
   aby chybová hláška zůstala konzistentní napříč celým systémem.
3. **`return_bool=True` znamená úplné potlačení výjimek** — i těch
   neočekávaných. To je vědomý kompromis: v boolean módu chce volající
   jednoduchou odpověď ano/ne, ne traceback.

[▲ Nahoru](#-obsah)

---

### `is_valid`

Pohodlný wrapper nad `validate(..., return_bool=True)`.

**Parametry:**
* `value` (*Any*): hodnota k ověření.

**Návratová hodnota:**
* `bool` — `True`, pokud je hodnota platná, jinak `False`. Nikdy nevyhazuje
  výjimku.

**Příklad použití:**
```python
if Age.is_valid(-5):
    ...
else:
    print("Neplatný věk")
```

[▲ Nahoru](#-obsah)

---

### `normalize`

Normalizuje vstupní hodnotu podle metadat — řeší `None`, optimalizaci
identity defaultu a validaci v jednom kroku.

**Parametry:**
* `value` (*Any*): hodnota k normalizaci.
* `process_none` (*bool*, výchozí `False`): pokud `True`, `None` je nahrazen
  výchozí hodnotou místo vyhození chyby.

**Návratová hodnota:**
* `Any`: normalizovaná hodnota (buď výchozí instance, nebo validovaná
  vstupní hodnota).

**Výjimky:**
* `SimpleRuntimeError`, pokud hodnota je `None` a `process_none=False`,
  nebo pokud validace selže.

**Pod kapotou:**
```python
def normalize(cls, value, *, process_none=False):
    if value is None:
        if process_none:
            return cls.meta.default
        raise_missing_value_error(cls)

    try:
        if value == cls.meta.default:
            return cls.meta.default
    except Exception:
        pass

    cls.validate(value)
    return value
```

**Proč je `None` v celém systému zakázané:** kompozitní objekty počítají
svou hodnotu z vnitřních prvků (`_inners`) — kdyby některý z nich mohl být
`None`, nedal by se z něj spočítat výsledek. Metadata to už hlídají na
úrovni definice třídy (`_default` nesmí být `None`); `normalize` totéž
vynucuje za běhu u hodnot, které přicházejí od uživatele.

**Optimalizace identity defaultu:** pokud se vstupní hodnota rovná
defaultu, vrátí se přímo instance `cls.meta.default` místo nové validace.
To šetří zbytečnou práci a udržuje stabilní identitu pro opakovaně
používanou výchozí hodnotu. Porovnání je obalené v `try/except`, protože ne
každá hodnota musí být vůbec porovnatelná s defaultem (`==` může u
libovolného typu vyhodit výjimku) — v tom případě se prostě pokračuje rovnou
k plné validaci.

[▲ Nahoru](#-obsah)

---

### `bool_or_raise_validate_error`

Pomocná metoda určená **výhradně** pro použití uvnitř uživatelské
`_validate` — umožňuje psát stručná validační pravidla bez ručního skládání
strukturovaných výjimek.

**Parametry:**
* `value` (*Any*): validovaná hodnota.
* `problem` (*str*): lidsky čitelný popis, co je špatně.
* `return_bool` (*bool*, výchozí `False`): pokud `True`, vrátí `False`
  místo vyhození výjimky.

**Návratová hodnota:**
* `False`, pokud `return_bool=True`.

**Výjimky:**
* `SimpleRuntimeError` (`ValueError` jako podkladová výjimka), pokud
  `return_bool=False`.

**Příklad použití:**
```python
@classmethod
def _validate(cls, value, *, return_bool=False):
    if value < 0:
        return cls.bool_or_raise_validate_error(
            value, "Hodnota musí být nezáporná.", return_bool=return_bool
        )
    return True
```

Díky tomu, že metoda sama respektuje `return_bool`, stačí ji v `_validate`
jen `return`-out — nemusíš v uživatelském kódu psát vlastní `if/else` pro
boolean vs. exception mód.

[▲ Nahoru](#-obsah)

---

## Validační pipeline jako celek

Tři metody na sebe navazují v jasném pořadí:

```
validate_type  →  _validate (uživatelský hook, přes cls.meta.validate)  →  normalize
```

* `validate_type` — nejrychlejší, nejlevnější kontrola: sedí typ?
* `validate` — nadstavba nad `validate_type`, zapojuje doménová pravidla
  z `_validate`.
* `normalize` — nejvyšší úroveň, používaná při skutečném přiřazení hodnoty:
  řeší `None`, identitu defaultu, a nakonec zavolá `validate`.

Tahle vrstvená stavba znamená, že si můžeš vybrat přesně tu úroveň přísnosti
a chování, kterou zrovna potřebuješ — od surové typové kontroly až po plnou
normalizaci s fallbackem na default.

➡️ Pokračování: [README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md)

[▲ Nahoru](#-obsah)
