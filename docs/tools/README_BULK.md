# 📦 Bulk — Hromadné vytváření z různých zdrojů dat

Bulk nástroje řeší situaci "mám seznam specifikací (z JSON, CSV, YAML,
tabulky, nebo prostě Python objektů) a chci z nich najednou vyrobit sadu
blueprintů/instancí" — nadstavba nad
[`create_simple_object`](README_AUTOMATE_CREATORS.md#create_simple_object--univerzální-fasáda)
pro hromadné zpracování.

```
create_simple_object_bulk          (univerzální fasáda — detekuje formát vstupu)
└── create_simple_object_bulk_from_bulk_case_class  (společný jmenovatel všech cest)
    ├── ...from_dicts     ← ...from_json, ...from_yaml
    ├── ...from_table
    └── ...from_csv
```

Všechny konkrétní varianty (`from_json`, `from_yaml`, `from_csv`,
`from_table`, `from_dicts`) jsou veřejně dostupné, ale nemají vlastní
README soubor — jsou dost malé a úzce propojené, aby dávalo smysl je
popsat společně přímo tady.

---

## 🧭 Obsah

* [`BulkCase` — specifikace jedné položky](#bulkcase--specifikace-jedné-položky)
* [`create_simple_object_bulk` — univerzální fasáda](#create_simple_object_bulk--univerzální-fasáda)
* [`create_simple_object_bulk_from_bulk_case_class` — společný jmenovatel](#create_simple_object_bulk_from_bulk_case_class--společný-jmenovatel)
* [Konkrétní zdrojové parsery](#konkrétní-zdrojové-parsery)
  * [`..._from_dicts`](#_from_dicts)
  * [`..._from_json`](#_from_json)
  * [`..._from_yaml`](#_from_yaml)
  * [`..._from_table`](#_from_table)
  * [`..._from_csv`](#_from_csv)

---

## `BulkCase` — specifikace jedné položky

`BulkCase` je `dataclass` reprezentující **jednu** položku pro hromadné
vytváření — obsahuje stejné parametry jako `create_simple_object`, plus
vlastní validaci ve `__post_init__` a metodu, která ji spustí.

**Pole:** `class_name`, `default`, `inners`, `value_type`, `validate`,
`logic`, `decompose`, `return_instance`, `mixins`, `as_atom`, `mutable` —
1:1 se signaturou `create_simple_object`.

**Validace probíhá při vytvoření `BulkCase`, ne až při volání
`create_simple_object`:**

```python
def __post_init__(self):
    validate_class_name_is_str(self.class_name)

    if self.inners is UNSET:
        validate_constant_has_default(self.class_name, self.default)
        validate_constant_has_not_logic(self.class_name, self.logic)
        validate_constant_has_not_decompose(self.class_name, self.decompose)
    else:
        validate_composite_has_inners(self.class_name, self.inners)
        validate_composite_has_logic(self.class_name, self.logic)
        validate_composite_has_not_default(self.class_name, self.default)
```

**Proč validovat dřív, než se cokoliv vytváří:** u hromadného zpracování
(desítky až stovky položek najednou) je mnohem lepší UX odhalit chybnou
specifikaci **hned při sestavení seznamu `BulkCase` objektů**, ne až
uprostřed dávkového zpracování, kde by bylo nejasné, která položka a proč
selhala. Všimni si i **symetrických** párů kontrol — `_default` je
povinný pro konstantu a zakázaný pro kompozici, `_logic`/`inners` přesně
naopak — stejné pravidlo, jaké zná `SimpleObjectMetadata` (viz
[README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md#zakázaný-_default)),
jen aplikované o úroveň dřív.

**`create_simple_object()` metoda** je jen tenký runner — přeposílá
uložené hodnoty do funkce se stejným jménem:

```python
def create_simple_object(self):
    return create_simple_object(
        class_name=self.class_name, default=self.default, inners=self.inners,
        value_type=self.value_type, validate=self.validate, logic=self.logic,
        decompose=self.decompose, return_instance=self.return_instance,
        mixins=self.mixins, as_atom=self.as_atom, mutable=self.mutable,
    )
```

`BulkCase` tedy funguje jako **odložené volání** — nese v sobě všechny
parametry i po validaci, a skutečné vytvoření třídy/instance se spustí až
později, typicky ve smyčce přes celý seznam.

[▲ Nahoru](#-obsah)

---

## `create_simple_object_bulk` — univerzální fasáda

**Parametry:** `source` (*Any*) — vstup libovolného podporovaného formátu.

**Návratová hodnota:** `list` vytvořených blueprintů/instancí.

**Detekční pravidla, v pořadí, v jakém se testují:**

```
source je list/tuple?
├─ prázdný           → from_dicts([])
├─ první prvek BulkCase  → from_bulk_case_class
├─ první prvek dict      → from_dicts
└─ první prvek list/tuple → from_table  (2D matice)

source je str?
├─ začíná "["                                → from_json
├─ první řádek obsahuje "class_name" a "," nebo ";" → from_csv
└─ jinak                                     → from_yaml (záložní pokus)
```

**Detekce podle prvního prvku, ne podle typové anotace.** Funkce
nevyžaduje, aby uživatel řekl, jaký formát posílá — pozná to sama podle
tvaru dat: `isinstance(first_item, BulkCase)`, `isinstance(first_item,
dict)`, `isinstance(first_item, (list, tuple))`. Tohle je pohodlné pro
uživatele (jedna funkce na cokoliv), ale znamená to, že u sekvenčních
vstupů rozhoduje **jen první prvek** — směšovaný seznam (např. `dict` a
pak `BulkCase` pohromadě) by fungoval nepředvídatelně, protože se prvky
za tím prvním nekontrolují dopředu.

**Detekce textového formátu je heuristická, s jasnou prioritou.** JSON má
nejsilnější signál (`cleaned.startswith("[")` — spolehlivé, protože bulk
vstup je vždy seznam). CSV se pozná podle přítomnosti hlavičky
`class_name` **a zároveň** oddělovače (`,`/`;`) na prvním řádku — dvojitá
podmínka snižuje riziko falešné shody. YAML je **záložní volba** — pokud
nic z předchozího nesedí, zkusí se YAML, protože YAML nemá tak
jednoznačný "podpis" jako JSON nebo CSV.

**Prázdný seznam je speciální případ** (`if not source: return
create_simple_object_bulk_from_dicts([])`) — bez tyhle výjimky by
`first_item = source[0]` na prázdné sekvenci spadlo na `IndexError`.

[▲ Nahoru](#-obsah)

---

## `create_simple_object_bulk_from_bulk_case_class` — společný jmenovatel

**Parametry:** `bulk_dicts` (*Iterable[BulkCase]*).

**Návratová hodnota:** `list` vytvořených blueprintů/instancí.

```python
def create_simple_object_bulk_from_bulk_case_class(bulk_dicts):
    results = []
    for index, item in enumerate(bulk_dicts):
        if not isinstance(item, BulkCase):
            raise_bulk_item_is_not_bulk_dict(item, index)
        results.append(item.create_simple_object())
    return results
```

**Tohle je místo, kam se sbíhají úplně všechny cesty** — bez ohledu na to,
jestli vstup byl JSON, CSV, YAML, tabulka, nebo přímý seznam `dict`, na
konci vždycky vznikne seznam `BulkCase` instancí a ten se zpracuje přesně
touhle jedinou funkcí. Každý ze specifických parserů níže tedy dělá jen
**jednu věc** — převede svůj specifický formát na `tuple[BulkCase, ...]` —
a zbytek (validace + vytvoření) nechává na týhle sdílené funkci.

`enumerate` s indexem v chybové hlášce (`raise_bulk_item_is_not_bulk_dict(item,
index)`) je důležitý detail pro hromadné zpracování — uživatel se
stovkami položek potřebuje vědět **která konkrétní** položka je
problematická, ne jen že "něco" nesedí.

[▲ Nahoru](#-obsah)

---

## Konkrétní zdrojové parsery

Všechny níže sdílí stejný závěrečný krok: sestaví `tuple[BulkCase, ...]`
a předají ho `create_simple_object_bulk_from_bulk_case_class`.

### `..._from_dicts`

```python
def create_simple_object_bulk_from_dicts(dicts):
    if not isinstance(dicts, (list, tuple)):
        raise_bulk_input_not_sequence(...)
    bulk = tuple(BulkCase(**d) for d in dicts)
    return create_simple_object_bulk_from_bulk_case_class(bulk)
```

Nejjednodušší a zároveň **základní stavební kámen** pro `from_json` a
`from_yaml` (obě formáty se nejdřív dekódují do Python `list[dict]` a pak
zavolají přesně tuhle funkci). Každý `dict` se rozbalí přímo jako
kwargs do `BulkCase(**d)` — klíče slovníku tedy musí odpovídat polím
`BulkCase` (`class_name`, `default`, `inners`, ...).

[▲ Nahoru](#-obsah)

### `..._from_json`

```python
def create_simple_object_bulk_from_json(json_string):
    if not isinstance(json_string, str):
        raise_bulk_input_not_str(json_string, "json")
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as exc:
        raise_bulk_decode_failed(json_string, "json", exc)
    if not isinstance(data, list):
        raise_bulk_data_not_list(data, "json")
    return create_simple_object_bulk_from_dicts(data)
```

Tři úrovně validace před tím, než se předá dál: typ vstupu (musí být
`str`), dekódovatelnost (`json.JSONDecodeError` se zachytí a přebalí do
strukturované chyby), a tvar výsledku (musí být `list`, ne třeba jeden
objekt). Teprve pak deleguje na `..._from_dicts`.

[▲ Nahoru](#-obsah)

### `..._from_yaml`

```python
def create_simple_object_bulk_from_yaml(yaml_string):
    if not isinstance(yaml_string, str):
        raise_bulk_input_not_str(yaml_string, "yaml")
    try:
        import yaml
    except ImportError:
        raise_bulk_yaml_import_failed()
    try:
        data = yaml.safe_load(yaml_string)
    except Exception as exc:
        raise_bulk_decode_failed(yaml_string, "yaml", exc)
    if not isinstance(data, list):
        raise_bulk_data_not_list(data, "yaml")
    return create_simple_object_bulk_from_dicts(data)
```

Stejná struktura jako `..._from_json`, jen s jedním extra krokem:
**volitelná závislost.** `import yaml` je uvnitř `try`, protože PyYAML
není povinný balíček celé knihovny — pokud uživatel YAML vůbec nepoužívá,
nemusí ho mít nainstalovaný. Pokud chybí a uživatel se pokusí o YAML
vstup, dostane srozumitelnou chybu (`raise_bulk_yaml_import_failed`)
místo suchého `ModuleNotFoundError`. `yaml.safe_load` (ne `yaml.load`) je
záměrná bezpečnostní volba — bezpečný parser, který nespouští libovolný
Python kód zakódovaný v YAML dokumentu.

[▲ Nahoru](#-obsah)

### `..._from_table`

```python
def create_simple_object_bulk_from_table(table):
    if not isinstance(table, (list, tuple)):
        raise_bulk_input_not_sequence(...)

    bulk = []
    for index, row in enumerate(table):
        if not isinstance(row, (list, tuple)):
            raise_bulk_table_row_not_sequence(row, index)

        def _get(idx, default=UNSET):
            return row[idx] if len(row) > idx else default

        bulk.append(BulkCase(
            class_name=_get(0), default=_get(1), value_type=_get(2),
            validate=_get(3), logic=_get(4), decompose=_get(5),
            return_instance=_get(6, False),
        ))

    return create_simple_object_bulk_from_bulk_case_class(tuple(bulk))
```

Formát "2D matice" — každý řádek je pozičně mapovaný na pole `BulkCase`
(`[0]` = `class_name`, `[1]` = `default`, atd.), bez pojmenovaných klíčů.
Pomocná uzavřená funkce `_get(idx, default=UNSET)` řeší **řádky různé
délky** — pokud řádek nemá dost prvků na všechny pozice, chybějící se
doplní `UNSET` (nebo `False` pro `return_instance`), místo aby to
spadlo na `IndexError`. Tenhle formát je nejúspornější zápis (žádné
klíče, jen hodnoty), ale je nejcitlivější na pořadí — proto je vhodný
hlavně pro programově generovaná data, ne pro ruční psaní.

[▲ Nahoru](#-obsah)

### `..._from_csv`

```python
def create_simple_object_bulk_from_csv(csv_string):
    if not isinstance(csv_string, str):
        raise_bulk_input_not_str(csv_string, "csv")

    reader = csv.DictReader(csv_string.strip().splitlines())
    bulk = []
    for row in reader:
        converted = {
            "class_name": row.get("class_name"),
            "default": _convert_value(row.get("default")),
            "value_type": _convert_type(row.get("value_type")),
            "validate": _convert_callable(row.get("validate"), "validate"),
            ...
        }
        bulk.append(BulkCase(**converted))

    return create_simple_object_bulk_from_bulk_case_class(tuple(bulk))
```

Nejsložitější parser, protože CSV je **čistě textový formát** — každá
hodnota musí projít explicitní konverzí z řetězce na skutečný Python typ:

* **`_convert_value`** — postupně zkusí `int`, pak `float`, pak nechá jako
  `str`; prázdný řetězec se stane `UNSET` (ne `None` — `None` má v systému
  jiný, striktně definovaný význam, viz
  [README_SIMPLE_CONSTANT.md](README_SIMPLE_CONSTANT.md#normalize)).
* **`_convert_type`** — mapuje textové jméno typu (`"int"`, `"str"`,
  `"float"`, `"bool"`) na skutečný typový objekt; neznámé jméno se
  ztlumí na `Any`, ne na chybu.
* **`_convert_bool`** — rozpozná `"true"`, `"1"`, `"yes"` (case-insensitive)
  jako `True`, cokoliv jiného jako `False`.
* **`_convert_callable`** — CSV **neumí přenést funkce/lambdy jako text**
  bezpečně (byl by to `exec` na cizím vstupu), takže pokud sloupec
  `validate`/`logic`/`decompose` obsahuje cokoliv, funkce rovnou vyhodí
  `raise_bulk_csv_callable_not_supported` — jasná, explicitní hranice
  toho, co CSV formát podporuje, místo tichého selhání nebo
  bezpečnostního rizika.

CSV je tedy vhodné hlavně pro **jednoduché konstanty** (kde stačí
`class_name`, `default`, `value_type`) — jakmile potřebuješ vlastní
validaci nebo logiku, je potřeba sáhnout po JSON/YAML (kde by ale funkce
musely existovat jako importovatelné objekty, ne jako text) nebo po
přímém `BulkCase`/Python API.

[▲ Nahoru](#-obsah)
