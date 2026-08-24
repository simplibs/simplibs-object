# 🧱 `SimpleBaseMetadata` — Základ pro veškerá metadata

`SimpleBaseMetadata` je společný předek pro `SimpleConstantMetadata`
a `SimpleObjectMetadata`. Sama o sobě nepočítá žádná doménová data (typ,
default, `_inners`...) — stará se výhradně o věci, které potřebuje **úplně
každá** metadata instance: identitu jména, evidenci jmenného prostoru,
čitelnou cestu v hierarchii a immutabilitu.

```
SimpleBaseMetadata           ← jsi tady
├── SimpleConstantMetadata
│   └── SimpleObjectMetadata
```

---

## 🧭 Obsah

* [Inicializační pipeline](#inicializační-pipeline)
* [Jmenná identita (`create_names`)](#jmenná-identita-create_names)
* [Cesta v hierarchii (`calculate_blueprint_path`)](#cesta-v-hierarchii-calculate_blueprint_path)
* [Write-once pravidlo](#write-once-pravidlo)
* [Architektura podtříd](#architektura-podtříd)

---

## Inicializační pipeline

```python
def __init__(self, owner_class):
    self.owner_class = owner_class
    self.class_name = owner_class.__name__
    (self.name_tuple, self.name_snake, self.name_private) = create_names(owner_class)
    self.node_names_set = {self.name_snake}
    self.blueprint_path = calculate_blueprint_path(owner_class)
    self._process_user_data()
```

Pět deterministických kroků, vždy ve stejném pořadí:

1. **Reference na vlastníka** — `owner_class`, tedy třída, pro kterou se
   metadata počítají.
2. **Jmenná identita** — čtyři odvozené varianty jména třídy (viz níže).
3. **Evidence jmenného prostoru** (`node_names_set`) — začíná jako
   jednoprvková množina obsahující vlastní `name_snake`. Podtřídy
   (`SimpleObjectMetadata`) ji při zpracování `_inners` rozšiřují o jména
   všech vnořených prvků — to je mechanismus, kterým systém hlídá **globálně
   unikátní jména napříč celým stromem kompozice** (viz
   [README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md#kolize-jmen)).
4. **Blueprint path** — čitelná reprezentace pozice v hierarchii dědičnosti.
5. **Hook pro podtřídy** (`_process_user_data`) — prázdná metoda, kterou
   přepisují `SimpleConstantMetadata`/`SimpleObjectMetadata` se svou
   vlastní doménovou logikou.

[▲ Nahoru](#-obsah)

---

## Jmenná identita (`create_names`)

`create_names` vygeneruje ze jména třídy tři odvozené varianty, každou pro
jiný účel:

| Varianta | Formát | Účel |
|---|---|---|
| `name_tuple` | `("My", "HTTP", "Client")` | sémantické jednotky se zachovanou kapitalizací |
| `name_snake` | `"my_http_client"` | jména parametrů, interní klíče |
| `name_private` | `"_my_http_client"` | privátní sloty a interní atributy |

Princip je **"nejdřív rozděl, pak normalizuj"**: `_class_name_splitter`
rozseká PascalCase jméno na sémantické jednotky (a při tom validuje, že
jméno je platný identifikátor, čistě ASCII a bez podtržítek), zatímco
`create_names` teprve tyhle jednotky spojí a znormalizuje na `snake_case`.
Rozdělení zodpovědností je striktní — splitter nezná pojem "snake_case",
`create_names` nezná pravidla dělení PascalCase.

**Rozpoznávání hranic slov** ve splitteru zvládá i akronymy:

```text
MyClass       → ("My", "Class")
HTTPServer    → ("HTTP", "Server")
User123       → ("User", "123")
MyHTTPClient  → ("My", "HTTP", "Client")
```

Klíčový trik je v chování na hranici akronym → slovo (`HTTPServer`): když
po sérii velkých písmen přijde malé písmeno, poslední velké písmeno se
"vrátí zpět" a stane se začátkem nového slova (`Server`), zatímco zbytek
(`HTTP`) se uzavře jako samostatná jednotka. Bez tohohle kroku by
`HTTPServer` skončilo jako jedno slovo, ne jako dvě.

Všechny tři varianty jsou **navzájem odvozené, ne nezávisle sestavené** —
`name_snake` vždy vychází z `name_tuple`, `name_private` vždy z
`name_snake`. To garantuje, že mezi nimi nikdy nemůže vzniknout
nekonzistence.

[▲ Nahoru](#-obsah)

---

## Cesta v hierarchii (`calculate_blueprint_path`)

Vytváří čitelnou reprezentaci dědičnosti pro účely `__repr__` (viz
[README_SIMPLE_META.md](README_SIMPLE_META.md#__repr__-a-__str__--reprezentace)) —
ukazuje, ze kterých **doménových** (ne systémových) rodičů třída dědí.

```python
def calculate_blueprint_path(cls):
    from .....SimpleBase import SimpleBase
    parents = [
        base.__name__ for base in cls.__mro__
        if issubclass(base, SimpleBase)
        and base.__name__ not in BASE_CLASS_NAMES
        and base is not cls
    ]
    return cls.__name__ if not parents else f"{cls.__name__}({', '.join(parents)})"
```

Filtruje MRO (`__mro__`) na tři podmínky zároveň: rodič musí být součástí
Simple ekosystému (`issubclass(base, SimpleBase)`), nesmí to být
framework-samotný kořen (`SimpleBase`/`SimpleConstant`/`SimpleObject` z
`BASE_CLASS_NAMES`) a nesmí to být třída sama.

| Hierarchie | Výstup |
|---|---|
| `MyConstant(SimpleConstant)` | `"MyConstant"` |
| `MyObject(BaseObject, SimpleObject)` | `"MyObject(BaseObject)"` |
| `Child(ParentA, ParentB, SimpleObject)` | `"Child(ParentA, ParentB)"` |

Import `SimpleBase` je záměrně lokální (uvnitř funkce) — zabraňuje to
cyklické závislosti při raném importu metadatového modulu, kdy
`SimpleBase` sám ještě může být ve fázi definice.

[▲ Nahoru](#-obsah)

---

## Write-once pravidlo

```python
def __setattr__(self, attr_name, new_value):
    current_value = getattr(self, attr_name, UNSET)
    if current_value is not UNSET:
        raise_metadata_is_immutable(attr_name, current_value, new_value, self.owner_class)
    super().__setattr__(attr_name, new_value)
```

Stejný princip jako u `SimpleMeta.__setattr__` na úrovni tříd (viz
[README_SIMPLE_META.md](README_SIMPLE_META.md#__setattr__--write-once-ochrana)),
tady aplikovaný na úrovni **instance metadat**: pole smí být nastaveno
právě jednou. Dokud má hodnotu `UNSET`, přiřazení projde; jakmile je jednou
nastavené, další pokus o zápis vyhodí `raise_metadata_is_immutable`.

Tohle je důvod, proč `__slots__` v `SimpleBaseMetadata` obsahuje jen jména
polí (`owner_class`, `class_name`, ...) bez výchozích hodnot — pole
"neexistují", dokud je `__init__` (respektive `_process_user_data`)
skutečně nenastaví, a `getattr(self, attr_name, UNSET)` vrátí `UNSET` pro
cokoliv, co ještě nebylo přiřazeno.

[▲ Nahoru](#-obsah)

---

## Architektura podtříd

Klíčové pravidlo pro každého, kdo by chtěl rozšířit metadatový systém:
**podtřídy nesmí přepisovat `__init__`.** Veškerá vlastní inicializace patří
do `_process_user_data()`.

Díky tomu je garantované, že:

* jmenná identita se vždy spočítá stejným způsobem,
* `node_names_set` se vždy inicializuje konzistentně,
* `blueprint_path` se vždy vygeneruje,
* struktura metadat je napříč celým systémem předvídatelná.

`SimpleBaseMetadata` samotná je záměrně odlehčená — veškerá těžká logika je
delegovaná do specializovaných procesorů (`create_names`,
`calculate_blueprint_path`, a v podtřídách `process_type`,
`process_default_for_constant`, `process_inners`, `process_classmethod`).
Metadata objekt se vytváří jednou za třídu a nikdy se nemutuje.

➡️ Pokračování: [README_SIMPLE_CONSTANT_METADATA.md](README_SIMPLE_CONSTANT_METADATA.md)

[▲ Nahoru](#-obsah)
