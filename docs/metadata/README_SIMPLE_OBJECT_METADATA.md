# 🧩 `SimpleObjectMetadata` — Kompilátor metadat pro kompozice

`SimpleObjectMetadata` dědí ze `SimpleConstantMetadata` (a tím pádem i ze
`SimpleBaseMetadata`) a rozšiřuje ji o vše, co potřebuje kompozice: validaci
`_inners`, vazbu na `_logic`/`_decompose`, odvození výchozí hodnoty a líné
vytváření kompozitních instančních tříd.

```
SimpleBaseMetadata
└── SimpleConstantMetadata
    └── SimpleObjectMetadata   ← jsi tady
```

Protože je to podtřída `SimpleConstantMetadata`, automaticky dědí i pole
jako `value_type`/`value_type_name` a mechanismus zpracování `_validate` —
viz [README_SIMPLE_CONSTANT_METADATA.md](README_SIMPLE_CONSTANT_METADATA.md).
Tenhle dokument popisuje jen to, co `SimpleObjectMetadata` přidává navíc.

---

## 🧭 Obsah

* [`_process_user_data` — inicializační pipeline](#_process_user_data--inicializační-pipeline)
* [Zakázaný `_default`](#zakázaný-_default)
* [Zpracování vnitřních prvků (`process_inners`)](#zpracování-vnitřních-prvků-process_inners)
* [Kolize jmen](#kolize-jmen)
* [Sestavení lookup map](#sestavení-lookup-map)
* [Zpracování `_logic` a odvození defaultu](#zpracování-_logic-a-odvození-defaultu)
* [Zpracování `_decompose` a dekomponovatelnost](#zpracování-_decompose-a-dekomponovatelnost)
* [Líné vytváření kompozitních tříd](#líné-vytváření-kompozitních-tříd)

---

## `_process_user_data` — inicializační pipeline

Jedenáct kroků, opět spuštěných jednou při definici třídy:

```python
def _process_user_data(self):
    self.is_constant = False                                    # 1
    if "_default" in self.owner_class.__dict__:                 # 2
        raise_default_is_defined_in_composition(self.owner_class)
    self.value_type, self.value_type_name = process_type(...)   # 3
    inners, node_names_set = process_inners(...)                # 4
    self.inners = inners
    self.node_names_set.update(node_names_set)
    self.inners_map = {...}                                     # 5
    self.inners_params_name = (...)
    inners_default = (...)                                      # 6
    inners_annotations = {...}
    self.logic, self.default = process_classmethod(...)         # 7
    self.decompose = process_classmethod(...)                   # 8
    self.is_decomposeable = (...)                                # 9
    self.validate = process_classmethod(...)                    # 10
    self._atom_class_mutable = UNSET                            # 11
    self._atom_class_immutable = UNSET
    self._composite_class_mutable = UNSET
    self._composite_class_immutable = UNSET
```

Pořadí kroků tu není náhodné — `_logic` (krok 7) potřebuje mít předem
hotové `inners_default`/`inners_annotations` z kroku 6, `_decompose`
(krok 8) potřebuje mít hotový `self.default` z kroku 7 (jako testovací
hodnotu pro dry-run) a `is_decomposeable` (krok 9) potřebuje mít hotové
oboje.

[▲ Nahoru](#-obsah)

---

## Zakázaný `_default`

```python
if "_default" in self.owner_class.__dict__:
    raise_default_is_defined_in_composition(self.owner_class)
```

Tohle je úplně první doménová kontrola, ještě před zpracováním typu nebo
`_inners` — kompozice **nesmí** sama definovat `_default`. Kontrola je
záměrně na `self.owner_class.__dict__` (jen lokální namespace), ne na
`hasattr` — kdyby se kontrolovalo přes `hasattr`, narazilo by to i na
zděděné `_default` ze `SimpleConstant` (kde má hodnotu `UNSET` jako
placeholder) a blokovalo by to úplně všechno.

**Proč je tohle pravidlo nekompromisní:** default kompozice musí být vždy
odvozený z `_logic(defaulty _inners)` (viz
[README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#důležité-_default-se-nesmí-definovat)).
Ruční `_default` by vytvořil dva konkurující zdroje pravdy — jeden
deklarovaný, jeden vypočítaný — a nebylo by garantováno, že jsou shodné.
Chybová hláška z `raise_default_is_defined_in_composition` navíc rovnou radí,
jak třídu opravit: buď `_default` odstranit, nebo (pokud byl záměr jiný)
odstranit `_inners`/`_logic` a udělat z třídy obyčejnou konstantu.

[▲ Nahoru](#-obsah)

---

## Zpracování vnitřních prvků (`process_inners`)

**Invariant, na kterém celá funkce stojí:** díky tomu, jak `SimpleMeta.__new__`
směruje třídy (`hasattr(cls, "_inners")` rozhoduje mezi `SimpleObjectMetadata`
a `SimpleConstantMetadata`), `process_inners` se vůbec nespustí, pokud
`_inners` neexistuje — funkce si tedy může dovolit rovnou `getattr(owner_class,
"_inners")` bez fallbacku na `UNSET`.

**Optimalizace: validovat jen lokálně deklarované `_inners`.**
```python
need_validations = "_inners" in owner_class.__dict__
```
Pokud třída `_inners` jen zdědila (nedefinovala je znovu sama), validace se
přeskočí — byly už jednou ověřené na rodičovské třídě a nemá smysl to dělat
znovu. Tenhle vzor (`need_validations` na základě lokální přítomnosti
klíče) se opakuje napříč metadatovým systémem, viz i
[`verify_classmethod`](README_METHOD_PROCESSING.md#verify_classmethod--brána-validovat-klonovat-nebo-zdědit).

**Validace, které proběhnou (jen když `need_validations`):**
* `_inners` musí být `tuple` a nesmí být prázdný,
* každý prvek musí být třída, musí dědit ze `SimpleConstant` a nesmí to být
  přímo `SimpleConstant`/`SimpleObject` samotné (jen konkrétní podtřídy).

[▲ Nahoru](#-obsah)

---

## Kolize jmen

Systém garantuje **globálně unikátní jména napříč celým stromem
kompozice** — dva různé vnitřní prvky (i v různých úrovních zanoření) nikdy
nesmí mít stejné `name_snake`. Mechanismus:

```python
new_node_names_set = node_names_set.copy()

for inner in raw_inners:
    node_name_collisions = new_node_names_set & inner.meta.node_names_set
    if node_name_collisions:
        collision_name = next(iter(node_name_collisions))
        validate_if_collision_with_owner_class(...)
        if need_validations:
            validate_collision_within_inners(...)
    new_node_names_set.update(inner.meta.node_names_set)
```

Průnik množin (`&`) mezi tím, co je dosud zaregistrované, a jmenným
prostorem nově přidávaného `inner` (`inner.meta.node_names_set` — což
zahrnuje i všechna jména *zanořená uvnitř* toho inner, ne jen jeho vlastní
jméno) okamžitě odhalí kolizi na jakékoliv hloubce. Rozlišují se dva druhy
kolize: s vlastníkem samotným (`validate_if_collision_with_owner_class`) a
mezi sourozeneckými `_inners` navzájem (`validate_collision_within_inners`).

**Namespace se šíří inkrementálně** — `new_node_names_set` je kopie
rodičovské množiny (`node_names_set.copy()`, aby se zabránilo "znečištění"
sourozeneckých podstromů) a po každém zpracovaném `inner` se aktualizuje
(`update`), takže každý další `inner` ve stejné iteraci už vidí jména všech
předchozích.

[▲ Nahoru](#-obsah)

---

## Sestavení lookup map

```python
self.inners_map = {inner.meta.name_snake: inner for inner in self.inners}
self.inners_params_name = tuple(inner.meta.name_snake for inner in self.inners)
```

Tyhle dvě struktury jsou to, co používá `_process_calculate_value_params`
při volání `calculate_value` (viz
[README_SIMPLE_OBJECT.md](README_SIMPLE_OBJECT.md#calculate_value)) —
`inners_map` pro mapování jméno → třída (validace, defaulty),
`inners_params_name` pro odvození očekávané signatury `_logic`.

[▲ Nahoru](#-obsah)

---

## Zpracování `_logic` a odvození defaultu

```python
inners_default = tuple(inner.meta.default for inner in self.inners)
inners_annotations = {inner.meta.name_snake: inner.meta.value_type for inner in self.inners}

self.logic, self.default = process_classmethod(
    method_name="_logic",
    expected_params=("cls", *self.inners_params_name),
    expected_args_params_count=1 + len(self.inners_params_name),
    expected_args_defaults=inners_default,
    expected_kwargs_defaults={},
    expected_param_types=inners_annotations,
    expected_return_type=self.value_type,
    owner_class=self.owner_class,
    return_calculated_value=True,
)
```

Očekávaná signatura `_logic` se **sestavuje dynamicky** z `_inners` —
`expected_params` je `("cls",)` plus jméno každého vnitřního prvku, ve
stejném pořadí. Díky `return_calculated_value=True` vrací
`process_classmethod` dvojici `(metoda, hodnota)` — a `self.default` je
přesně ten výsledek dry-runu s výchozími hodnotami všech `_inners`. Tohle
je konkrétní místo v kódu, kde platí pravidlo zmíněné výše: *default
kompozice = `_logic(defaulty _inners)`*, spočítané jednou při definici
třídy a od teď fixní.

Kompletní popis, jak samotné `process_classmethod` metodu ověřuje (kontrola
signatury, anotací, dry-run), je v
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md).

[▲ Nahoru](#-obsah)

---

## Zpracování `_decompose` a dekomponovatelnost

```python
self.decompose = process_classmethod(
    method_name="_decompose",
    expected_params=("cls", "value"),
    expected_args_params_count=2,
    expected_args_defaults=(self.default,),
    expected_kwargs_defaults={},
    expected_param_types={"value": self.value_type},
    expected_return_type=tuple,
    owner_class=self.owner_class,
)

self.is_decomposeable = (
    self.decompose is not UNSET
    and all(inner.meta.is_constant or inner.meta.is_decomposeable for inner in self.inners)
)
```

`_decompose` je volitelný — pokud ho uživatel nedefinuje,
`process_classmethod` (přes `verify_classmethod`, viz
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md#verify_classmethod--brána-validovat-klonovat-nebo-zdědit))
vrátí `UNSET`, aniž by spouštěl dry-run.

**`is_decomposeable` je rekurzivní podmínka, ne jen lokální kontrola.**
Nestačí, že tahle konkrétní třída definuje `_decompose` — kompozice je
dekomponovatelná jen tehdy, pokud **úplně každý** její vnitřní prvek buď
je konstanta (`inner.meta.is_constant`, atomy jsou triviálně
"dekomponovatelné" samy do sebe), nebo je to sama dekomponovatelná
kompozice (`inner.meta.is_decomposeable`). Jinými slovy: řetězec
dekomponovatelnosti se musí táhnout přes celý strom, jinak by zpětná
dekompozice na nejnižší úrovni "uvázla".

[▲ Nahoru](#-obsah)

---

## Líné vytváření kompozitních tříd

```python
@property
def composite_class_mutable(self):
    if self._composite_class_mutable is UNSET:
        self._composite_class_mutable = make_composite_class(self.owner_class.__metadata__)
    return self._composite_class_mutable
```

Stejný lazy vzor jako u `atom_class_mutable`/`atom_class_immutable` v
`SimpleConstantMetadata` — skutečná runtime třída se kompiluje (přes
`make_composite_class`) až při prvním přístupu.

Hlubší popis toho, co přesně `make_composite_class` sestavuje (dědičnost
z atomické třídy, sloty pro `_inners`, reaktivní hooky), bude
v navazujícím README o vytváření instancí.

[▲ Nahoru](#-obsah)
