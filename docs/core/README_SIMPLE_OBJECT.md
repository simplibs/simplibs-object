# 🧩 `SimpleObject` — Deklarativní kompozice

`SimpleObject` rozšiřuje `SimpleConstant` o schopnost skládat hodnotu
z vnitřních prvků (`_inners`). Je to vlajková třída celého systému —
umožňuje deklarativně, typově bezpečně a deterministicky modelovat
strukturovaná data, kde se výsledná hodnota vždy počítá z prvků, ze kterých
je kompozice postavená.

```
SimpleBase
└── SimpleConstant
    └── SimpleObject   ← jsi tady (dědí VŠE ze SimpleConstant)
```

Protože `SimpleObject` dědí ze `SimpleConstant`, každá kompozice automaticky
umí i vše z [README_SIMPLE_CONSTANT.md](README_SIMPLE_CONSTANT.md) —
`validate`, `normalize`, `is_valid` atd. Tenhle dokument popisuje jen to, co
`SimpleObject` přidává navíc.

---

## 🧭 Obsah

* [Deklarativní rozhraní](#deklarativní-rozhraní)
  * [`_type`](#_type)
  * [`_inners`](#_inners)
  * [`_logic`](#_logic)
  * [`_decompose`](#_decompose)
  * [`_validate`](#_validate)
* [Důležité: `_default` se nesmí definovat](#důležité-_default-se-nesmí-definovat)
* [Veřejné API](#veřejné-api)
  * [`calculate_value`](#calculate_value)
  * [`decompose_value`](#decompose_value)
* [Architektonická role](#architektonická-role)

---

## Deklarativní rozhraní

```python
class FullName(SimpleObject):
    _type = str
    _inners = (FirstName, LastName)

    @classmethod
    def _logic(cls, first_name, last_name):
        return f"{first_name} {last_name}"

    @classmethod
    def _decompose(cls, value):
        first, _, last = value.partition(" ")
        return (first, last)
```

### `_type`

Typová anotace pro **výsledek** kompozice. Výstup `_logic` musí projít
stejnou plnou validací jako u atomu (viz
[validační pipeline](README_SIMPLE_CONSTANT.md#validační-pipeline-jako-celek)).

### `_inners`

Povinný tuple vnitřních prvků — každý je buď `SimpleConstant`, nebo další
`SimpleObject` (kompozice se tedy mohou vnořovat do libovolné hloubky).
Struktura `_inners` určuje:

* jaké parametry očekává `_logic`,
* jakou má kompozice výchozí hodnotu (spočte se z defaultů vnitřních prvků),
* zda kompozice podporuje zpětnou dekompozici,
* rozvržení metadat celé kompozice.

### `_logic`

Povinný výpočetní hook — definuje, jak se z vnitřních prvků spočítá
výsledná hodnota kompozice. Přijímá parametry odpovídající `_inners`
(podle jména, ne jen podle pozice) a musí vrátit hodnotu, která projde plnou
validací.

**Výchozí hodnota celé kompozice** se počítá automaticky zavoláním `_logic`
s defaulty všech vnitřních prvků — proto kompozice nikdy sama nedefinuje
`_default` (viz [níže](#důležité-_default-se-nesmí-definovat)).

### `_decompose`

Volitelný hook pro opačný směr — převede hotovou hodnotu kompozice zpět na
hodnoty pro jednotlivé vnitřní prvky. Umožňuje obousměrné modely: nahoru
(vnitřní prvky → kompozice) i dolů (kompozice → vnitřní prvky). Pokud ho
uživatel nedefinuje, kompozice je považována za nedekomponovatelnou.

### `_validate`

Stejný hook jako u `SimpleConstant` — volitelná rozšířená validace nad
rámec typové kontroly, se stejnými třemi možnostmi (vrátit bool, vyhodit
výjimku, nebo použít `bool_or_raise_validate_error`).

[▲ Nahoru](#-obsah)

---

## Důležité: `_default` se nesmí definovat

Na rozdíl od `SimpleConstant` kompozice **nikdy** nedefinuje `_default`
sama — metadata to aktivně hlídají a při pokusu o definici vyhodí
strukturovanou chybu (`raise_default_is_defined_in_composition`, viz
`SimpleObjectMetadata`). Výchozí hodnota se vždy odvozuje automaticky:

```
_default kompozice = _logic(defaulty všech _inners)
```

Tohle pravidlo je záměrné a důležité: garantuje, že default kompozice je
vždy **konzistentní** s jejím vlastním výpočetním pravidlem — nemůže se
stát, že by si někdo ručně nastavil default, který neodpovídá tomu, co by
`_logic` doopravdy spočítala.

[▲ Nahoru](#-obsah)

---

## Veřejné API

Stejně jako u `SimpleConstant` jsou i tyhle metody tenké wrappery nad
interní logikou v `_core/logic/object_methods/`.

### `calculate_value`

Spočítá hodnotu kompozice zavoláním uživatelské `_logic`, s plným
zpracováním a validací parametrů před tím, než se `_logic` vůbec spustí.

**Parametry:**
* `*args`, `**kwargs`: hodnoty mapované na vnitřní prvky (podle pořadí
  v `_inners`, nebo podle jména).

**Návratová hodnota:**
* `Any`: spočítaná hodnota kompozice.

**Výjimky:**
* `SimpleRuntimeError`, pokud selže zpracování parametrů nebo validace.

**Zajímavost pro IDE:** signatura používá `ParamSpec` (`LogicSignature[P,
R]`), díky čemuž PyCharm (i jiná IDE) nabízí **automatické doplňování
přesně těch parametrů, které očekává tvoje `_logic`** — i když
`calculate_value` samo o sobě žádné konkrétní parametry nedeklaruje.

**Pod kapotou — zpracování parametrů (`_process_calculate_value_params`):**
```python
def _process_calculate_value_params(cls, *args, **kwargs):
    inners_map = cls.meta.inners_map

    if len(args) > len(inners_map):
        raise_too_many_positional_args_error(...)

    clean_kwargs = {}
    args_iter = iter(args)

    for param_name, inner_cls in inners_map.items():
        try:
            value = next(args_iter)
            if param_name in kwargs:
                raise_duplicate_argument_error(cls, param_name)
        except StopIteration:
            value = kwargs.pop(param_name, None)

        if value is None:
            value = inner_cls.meta.default
        else:
            inner_cls.validate(value)

        clean_kwargs[param_name] = value

    if kwargs:
        raise_unknown_parameter_error(cls, list(kwargs.keys()))

    return clean_kwargs
```

Tahle funkce dělá čtyři věci najednou a každou hlídá strukturovanou chybou:

1. **Kontrola počtu pozičních argumentů** — nesmí jich být víc, než kolik
   je vnitřních prvků.
2. **Detekce duplicit** — pokud je parametr zadaný poziční *i* klíčovým
   argumentem zároveň, je to chyba (ne tiché přepsání).
3. **Fallback na default** — chybějící parametr se doplní z
   `inner_cls.meta.default`, ne z nějaké obecné `None` hodnoty.
4. **Detekce neznámých klíčových argumentů** — cokoliv, co zbyde
   v `kwargs` po zpracování všech známých `_inners`, je chyba.

Samotné `calculate_value` pak už jen zavolá `cls.meta.logic(**params_dict)`
— veškerá složitost zpracování parametrů je schválně oddělená do vlastní
funkce, aby zůstalo čitelné, co dělá co.

[▲ Nahoru](#-obsah)

---

### `decompose_value`

Rozloží hotovou hodnotu kompozice zpět na hodnoty jejích vnitřních prvků,
pomocí uživatelské `_decompose`.

**Parametry:**
* `value` (*Any*): hodnota kompozice k rozložení.

**Návratová hodnota:**
* `Any`: rozložená reprezentace (typicky tuple hodnot pro `_inners`).

**Výjimky:**
* `SimpleRuntimeError`, pokud kompozice není dekomponovatelná, nebo pokud
  `value` neprojde validací.

**Pod kapotou:**
```python
def decompose_value(cls, value):
    if not cls.meta.is_decomposeable:
        raise_class_not_decomposeable(cls.meta)

    cls.validate(value)
    outcome = cls.meta.decompose(value)
    return outcome
```

Pořadí kroků tu není náhodné: nejdřív se ověří, že dekompozice vůbec dává
smysl (`is_decomposeable`), teprve pak se validuje vstupní `value` a až
nakonec proběhne samotné rozložení. Tohle pořadí zabraňuje zbytečné práci —
nemá smysl validovat hodnotu pro operaci, která stejně skončí chybou
"nedekomponovatelné".

[▲ Nahoru](#-obsah)

---

## Architektonická role

`SimpleObject` je vlajková třída celého Simple systému:

* deklarativní modelování složených struktur,
* deterministické odvozování výchozí hodnoty z vnitřních prvků,
* metadaty řízený výpočet (`calculate_value`) i volitelná zpětná dekompozice
  (`decompose_value`),
* plné dědictví validace a normalizace ze `SimpleConstant`,
* typově bezpečné, čitelné, deklarativní API — uživatel píše jen `_type`,
  `_inners`, `_logic` (a volitelně `_decompose`/`_validate`), zbytek
  (parsing parametrů, validace, chybové hlášky) obstará systém.

Skutečné vytváření běžících instancí z takhle definované třídy (atomické
i kompozitní, mutable i immutable varianty) je popsané v navazujícím
dokumentu o metadatech a instance builderech.

➡️ Pokračování: [README_SIMPLE_META.md](README_SIMPLE_META.md)

[▲ Nahoru](#-obsah)
