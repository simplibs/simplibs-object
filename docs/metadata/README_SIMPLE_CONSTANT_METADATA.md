# ⚛️ `SimpleConstantMetadata` — Kompilátor metadat pro atomy

`SimpleConstantMetadata` přebírá strukturu ze `SimpleBaseMetadata` (jméno,
jmenný prostor, blueprint path) a doplňuje ji o vše doménově specifické pro
konstanty: typ, default, validaci a líné vytváření atomických instančních
tříd.

```
SimpleBaseMetadata
└── SimpleConstantMetadata     ← jsi tady
    └── SimpleObjectMetadata
```

---

## 🧭 Obsah

* [`_process_user_data` — inicializační pipeline](#_process_user_data--inicializační-pipeline)
* [Zpracování typu (`process_type`)](#zpracování-typu-process_type)
* [Zpracování defaultu (`process_default_for_constant`)](#zpracování-defaultu-process_default_for_constant)
* [Zpracování `_validate`](#zpracování-_validate)
* [Líné vytváření atomických tříd](#líné-vytváření-atomických-tříd)

---

## `_process_user_data` — inicializační pipeline

```python
def _process_user_data(self):
    self.is_constant = True
    self.value_type, self.value_type_name = process_type(owner_class=self.owner_class)
    self.default = process_default_for_constant(
        default_type=self.value_type, owner_class=self.owner_class,
    )
    self.validate = process_classmethod(
        method_name="_validate",
        expected_params=("cls", "value", "return_bool"),
        expected_args_params_count=2,
        expected_args_defaults=(),
        expected_kwargs_defaults={"return_bool": False},
        expected_param_types={"value": Any, "return_bool": bool},
        expected_return_type=bool | None,
        test_value=(self.default,),
        owner_class=self.owner_class,
    )
    self._atom_class_mutable = UNSET
    self._atom_class_immutable = UNSET
```

Pět kroků, které se spustí přesně jednou, při definici uživatelské třídy:

1. **Označení jako konstanta** (`is_constant = True`) — `SimpleObjectMetadata`
   tohle později přepíše na `False`, viz
   [README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md).
2. **Zpracování `_type`** přes `process_type`.
3. **Zpracování `_default`** přes `process_default_for_constant` — všimni
   si, že jako `default_type` dostává přesně to, co vrátil krok 2, ne
   surové `_type` — typ je tedy vždy validovaný dřív, než se proti němu
   ověřuje default.
4. **Zpracování `_validate`** přes sdílenou pipeline `process_classmethod`
   (viz [README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md)).
   Testovací hodnota pro dry-run je `(self.default,)` — validace se tedy
   hned při definici třídy vyzkouší na výchozí hodnotě.
5. **Reset cache** pro atomické instanční třídy (viz níže).

[▲ Nahoru](#-obsah)

---

## Zpracování typu (`process_type`)

Normalizuje `_type` do jediné, předvídatelné runtime formy — bez ohledu na
to, jestli ho uživatel zapsal jako holý typ, moderní union, nebo tuple typů.

**Podporované vstupní formy:**

| Zápis `_type` | Rozpoznáno jako | Výsledek |
|---|---|---|
| `int` | atomický typ | vrací se okamžitě, beze změny |
| `int \| str` | `UnionType` | vrací se beze změny (po kontrole na `None`) |
| `(int, str)` | tuple typů | převedeno na `UnionType` přes `reduce(or_, ...)` |

**Pravidlo proti volitelnosti:** `_type` nikdy nesmí (přímo ani skrz
union/tuple) obsahovat `NoneType` — pokud ano, `process_type` vyhodí
`raise_union_type_contain_none`. Nepřítomnost hodnoty se v systému modeluje
jinde (na úrovni `normalize`/`process_none`, viz
[README_SIMPLE_CONSTANT.md](README_SIMPLE_CONSTANT.md#normalize)), nikdy
zamíchaná přímo do typové definice.

**Proč sjednocovat na `UnionType`:** zbytek systému pak může na typ vždy
zavolat obyčejné `isinstance(value, compiled_type)`, bez ohledu na to,
jestli šlo původně o jeden typ, union, nebo tuple — žádné větvení
podle "jaký byl vlastně vstupní formát" se nikde jinde v kódu nemusí řešit.

**Poznámka ke vstupu jako tuple:** na rozdíl od `UnionType` (kde se jen
kontroluje přítomnost `None`), u tuple se navíc kontroluje, že není
vnořená (`(int, (str, float))` je neplatné — `_type` musí být plochý) a že
neobsahuje doslovné `None` jako prvek.

[▲ Nahoru](#-obsah)

---

## Zpracování defaultu (`process_default_for_constant`)

```python
def process_default_for_constant(default_type, owner_class):
    raw_default = getattr(owner_class, "_default", UNSET)
    if raw_default is UNSET or not isinstance(raw_default, default_type):
        validate_default_is_defined(raw_default, owner_class)
        validate_default_matches_annotation(raw_default, default_type, owner_class)
    return raw_default
```

Krátká, ale důležitá funkce se dvěma pravidly: `_default` musí **existovat**
a musí **odpovídat typu** vypočítanému v `process_type`. Šťastná cesta
(`isinstance` sedí) se vrátí okamžitě bez volání validátorů — ty se spustí
jen v chybovém případě, aby poskytly přesnou diagnostiku.

Protože konstanty nemají žádnou vnitřní strukturu (na rozdíl od kompozic),
je `_default` jediným zdrojem jejich výchozí runtime identity — proto je
u konstant povinný, zatímco u kompozic je zakázaný (viz
[README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md#zakázaný-_default)).

[▲ Nahoru](#-obsah)

---

## Zpracování `_validate`

Kompletní popis toho, jak `process_classmethod` (a jeho vnitřní
verifikátory `verify_classmethod`, `verify_params`,
`verify_annotations_and_defaults`, `verify_calculation`) ověřuje a
normalizuje `_validate`, je ve sdíleném dokumentu
[README_METHOD_PROCESSING.md](README_METHOD_PROCESSING.md) — stejná
pipeline se beze změny používá i pro `_logic` a `_decompose` na
`SimpleObjectMetadata`.

[▲ Nahoru](#-obsah)

---

## Líné vytváření atomických tříd

```python
@property
def atom_class_mutable(self):
    if self._atom_class_mutable is UNSET:
        self._atom_class_mutable = make_atom_class(self.owner_class.__metadata__)
    return self._atom_class_mutable

@property
def atom_class_immutable(self):
    if self._atom_class_immutable is UNSET:
        self._atom_class_immutable = make_atom_class(
            self.owner_class.__metadata__, mutable=False,
        )
    return self._atom_class_immutable
```

Skutečné runtime třídy pro atomické instance (mutable i immutable varianta)
se **nevytváří automaticky při definici blueprintu** — vznikají líně, až
při prvním přístupu k příslušné property. `make_atom_class` (definovaná
v `_core/metadata/instance_builders/atom_class/`) pak zkompiluje konkrétní
runtime třídu přes `type(...)`.

Tenhle lazy přístup má jasný důvod: kompilace runtime třídy je relativně
drahá operace (sestavení `class_dict`, sloty, `__init__` closure...) a ne
každý blueprint někdy potřebuje obě varianty (mutable i immutable) — proč
tedy platit cenu za kompilaci, kterou možná nikdo nikdy nevyužije.

Hlubší popis toho, co přesně `make_atom_class` sestavuje, je
v navazujícím README o vytváření instancí.

➡️ Pokračování: [README_SIMPLE_OBJECT_METADATA.md](README_SIMPLE_OBJECT_METADATA.md)

[▲ Nahoru](#-obsah)
