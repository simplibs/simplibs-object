# 📦 Bulk — Batch creation from various data sources

The bulk tools handle the situation "I have a list of specs (from JSON,
CSV, YAML, a table, or plain Python objects) and I want to build a whole
batch of blueprints/instances from them at once" — an extension on top of
[`create_simple_object`](README_AUTOMATE_CREATORS.md#create_simple_object--the-universal-facade)
for batch processing.

```
create_simple_object_bulk          (universal facade — detects the input format)
└── create_simple_object_bulk_from_bulk_case_class  (the common denominator for every path)
    ├── ...from_dicts     ← ...from_json, ...from_yaml
    ├── ...from_table
    └── ...from_csv
```

All the specific variants (`from_json`, `from_yaml`, `from_csv`,
`from_table`, `from_dicts`) are publicly accessible, but don't have their
own README file — they're small enough and closely enough related that it
makes sense to cover them together, right here.

---

## 🧭 Contents

* [`BulkCase` — the specification for one item](#bulkcase--the-specification-for-one-item)
* [`create_simple_object_bulk` — the universal facade](#create_simple_object_bulk--the-universal-facade)
* [`create_simple_object_bulk_from_bulk_case_class` — the common denominator](#create_simple_object_bulk_from_bulk_case_class--the-common-denominator)
* [Concrete source parsers](#concrete-source-parsers)
  * [`..._from_dicts`](#_from_dicts)
  * [`..._from_json`](#_from_json)
  * [`..._from_yaml`](#_from_yaml)
  * [`..._from_table`](#_from_table)
  * [`..._from_csv`](#_from_csv)

[⬅️ Back to main README](../../README.md)

---

## `BulkCase` — the specification for one item

`BulkCase` is a `dataclass` representing **one** item for batch creation —
it holds the same parameters as `create_simple_object`, plus its own
validation in `__post_init__` and a method that runs it.

**Fields:** `class_name`, `default`, `inners`, `value_type`, `validate`,
`logic`, `decompose`, `return_instance`, `mixins`, `as_atom`, `mutable` —
1:1 with `create_simple_object`'s signature.

**Validation happens when the `BulkCase` is created, not when
`create_simple_object` is called:**

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

**Why validate before anything is created:** for batch processing (dozens
to hundreds of items at once), it's a much better user experience to catch
an invalid spec **right when the list of `BulkCase` objects is built**,
rather than in the middle of batch processing, where it would be unclear
which item failed and why. Notice also the **symmetrical** pairs of checks
— `_default` is required for a constant and forbidden for a composition,
`_logic`/`inners` exactly the reverse — the same rule
`SimpleObjectMetadata` already enforces (see
[README_SIMPLE_OBJECT_METADATA](../metadata/README_SIMPLE_OBJECT_METADATA.md#the-forbidden-_default)),
just applied one level earlier.

**The `create_simple_object()` method** is just a thin runner — it
forwards the stored values into the same-named function:

```python
def create_simple_object(self):
    return create_simple_object(
        class_name=self.class_name, default=self.default, inners=self.inners,
        value_type=self.value_type, validate=self.validate, logic=self.logic,
        decompose=self.decompose, return_instance=self.return_instance,
        mixins=self.mixins, as_atom=self.as_atom, mutable=self.mutable,
    )
```

`BulkCase` therefore works as a **deferred call** — it carries all its
parameters even after validation, and the actual class/instance creation
only runs later, typically in a loop over the whole list.

[▲ Back to Contents](#-contents)

---

## `create_simple_object_bulk` — the universal facade

**Parameters:** `source` (*Any*) — input in any supported format.

**Return value:** a `list` of created blueprints/instances.

**Detection rules, in the order they're tested:**

```
is source a list/tuple?
├─ empty                    → from_dicts([])
├─ first element is BulkCase  → from_bulk_case_class
├─ first element is dict      → from_dicts
└─ first element is list/tuple → from_table  (2D matrix)

is source a str?
├─ starts with "["                                  → from_json
├─ the first line contains "class_name" and "," or ";" → from_csv
└─ otherwise                                        → from_yaml (fallback attempt)
```

**Detection is based on the first element, not a type annotation.** The
function doesn't require the user to state which format they're sending —
it figures it out itself from the shape of the data:
`isinstance(first_item, BulkCase)`, `isinstance(first_item, dict)`,
`isinstance(first_item, (list, tuple))`. This is convenient for the user
(one function for everything), but it means that for sequence inputs,
**only the first element** decides the branch — a mixed list (e.g. a `dict`
followed by a `BulkCase`) would behave unpredictably, since elements after
the first aren't checked ahead of time.

**Text-format detection is heuristic, with a clear priority order.** JSON
has the strongest signal (`cleaned.startswith("[")` — reliable, since bulk
input is always a list). CSV is recognized by the presence of a
`class_name` header **and** a delimiter (`,`/`;`) on the first line at the
same time — the double condition lowers the risk of a false match. YAML is
the **fallback choice** — if none of the above matches, YAML is tried,
since YAML doesn't have as clear-cut a "signature" as JSON or CSV.

**An empty list is a special case** (`if not source: return
create_simple_object_bulk_from_dicts([])`) — without this exception,
`first_item = source[0]` on an empty sequence would raise `IndexError`.

[▲ Back to Contents](#-contents)

---

## `create_simple_object_bulk_from_bulk_case_class` — the common denominator

**Parameters:** `bulk_dicts` (*Iterable[BulkCase]*).

**Return value:** a `list` of created blueprints/instances.

```python
def create_simple_object_bulk_from_bulk_case_class(bulk_dicts):
    results = []
    for index, item in enumerate(bulk_dicts):
        if not isinstance(item, BulkCase):
            raise_bulk_item_is_not_bulk_dict(item, index)
        results.append(item.create_simple_object())
    return results
```

**This is the point where absolutely every path converges** — regardless
of whether the input was JSON, CSV, YAML, a table, or a plain list of
`dict`, at the end there's always a list of `BulkCase` instances, and it's
processed by this exact single function. So each of the specific parsers
below does only **one thing** — convert its specific format into a
`tuple[BulkCase, ...]` — and leaves the rest (validation + creation) to
this shared function.

`enumerate` with the index in the error message
(`raise_bulk_item_is_not_bulk_dict(item, index)`) is an important detail
for batch processing — a user with hundreds of items needs to know
**exactly which** item is problematic, not just that "something" doesn't
match.

[▲ Back to Contents](#-contents)

---

## Concrete source parsers

All of the below share the same final step: they build a
`tuple[BulkCase, ...]` and pass it to
`create_simple_object_bulk_from_bulk_case_class`.

### `..._from_dicts`

```python
def create_simple_object_bulk_from_dicts(dicts):
    if not isinstance(dicts, (list, tuple)):
        raise_bulk_input_not_sequence(...)
    bulk = tuple(BulkCase(**d) for d in dicts)
    return create_simple_object_bulk_from_bulk_case_class(bulk)
```

The simplest, and also the **fundamental building block** for `from_json`
and `from_yaml` (both formats are first decoded into a Python
`list[dict]`, and then this exact function is called). Each `dict` is
unpacked directly as kwargs into `BulkCase(**d)` — so the dictionary's
keys have to match `BulkCase`'s fields (`class_name`, `default`,
`inners`, ...).

[▲ Back to Contents](#-contents)

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

Three levels of validation before it's passed along further: the input
type (must be `str`), decodability (`json.JSONDecodeError` is caught and
wrapped into a structured error), and the shape of the result (must be a
`list`, not, say, a single object). Only then does it delegate to
`..._from_dicts`.

[▲ Back to Contents](#-contents)

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

Same structure as `..._from_json`, just with one extra step: an
**optional dependency.** `import yaml` sits inside a `try`, because PyYAML
isn't a required package for the whole library — if the user never uses
YAML, they don't need it installed. If it's missing and the user tries a
YAML input, they get a clear error (`raise_bulk_yaml_import_failed`)
instead of a dry `ModuleNotFoundError`. `yaml.safe_load` (not `yaml.load`)
is a deliberate security choice — a safe parser that doesn't execute
arbitrary Python code encoded in a YAML document.

[▲ Back to Contents](#-contents)

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

A "2D matrix" format — every row is positionally mapped to `BulkCase`'s
fields (`[0]` = `class_name`, `[1]` = `default`, etc.), with no named
keys. The helper closure `_get(idx, default=UNSET)` handles **rows of
different lengths** — if a row doesn't have enough elements for every
position, the missing ones are filled in with `UNSET` (or `False` for
`return_instance`), instead of raising `IndexError`. This format is the
most compact notation (no keys, just values), but it's the most
order-sensitive — so it's best suited for programmatically generated
data, not for hand-written input.

[▲ Back to Contents](#-contents)

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

The most complex parser, because CSV is a **purely textual format** —
every value has to go through explicit conversion from a string into an
actual Python type:

* **`_convert_value`** — tries `int`, then `float`, in order, and finally
  falls back to `str`; an empty string becomes `UNSET` (not `None` — `None`
  has a different, strictly defined meaning in the system, see
  [README_SIMPLE_CONSTANT](../core/README_SIMPLE_CONSTANT.md#normalize)).
* **`_convert_type`** — maps a type's text name (`"int"`, `"str"`,
  `"float"`, `"bool"`) to the actual type object; an unknown name falls
  back to `Any`, not an error.
* **`_convert_bool`** — recognizes `"true"`, `"1"`, `"yes"`
  (case-insensitive) as `True`, anything else as `False`.
* **`_convert_callable`** — CSV **can't safely carry functions/lambdas as
  text** (that would mean `exec`-ing untrusted input), so if the
  `validate`/`logic`/`decompose` column contains anything at all, the
  function immediately raises
  `raise_bulk_csv_callable_not_supported` — a clear, explicit boundary of
  what the CSV format supports, instead of a silent failure or a security
  risk.

CSV is therefore mainly suited for **simple constants** (where
`class_name`, `default`, `value_type` are enough) — as soon as you need
custom validation or logic, you have to reach for JSON/YAML (where,
though, the functions would need to exist as importable objects, not as
text) or for `BulkCase`/the direct Python API.

[▲ Back to Contents](#-contents)
