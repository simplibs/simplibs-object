# ⚛️ `SimpleConstantMetadata` — Metadata compiler for atoms

`SimpleConstantMetadata` takes over the structure from `SimpleBaseMetadata`
(name, namespace, blueprint path) and adds everything domain-specific to
constants: type, default, validation, and lazy creation of atomic instance
classes.

```
SimpleBaseMetadata
└── SimpleConstantMetadata     ← you are here
    └── SimpleObjectMetadata
```

---

## 🧭 Contents

* [`_process_user_data` — initialization pipeline](#_process_user_data--initialization-pipeline)
* [Type processing (`process_type`)](#type-processing-process_type)
* [Default processing (`process_default_for_constant`)](#default-processing-process_default_for_constant)
* [Processing `_validate`](#processing-_validate)
* [Lazy creation of atomic classes](#lazy-creation-of-atomic-classes)

[⬅️ Back to main README](../../README.md)

---

## `_process_user_data` — initialization pipeline

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

Five steps, run exactly once, when the user-defined class is defined:

1. **Marking it as a constant** (`is_constant = True`) —
   `SimpleObjectMetadata` later overrides this to `False`, see
   [README_SIMPLE_OBJECT_METADATA](README_SIMPLE_OBJECT_METADATA.md).
2. **Processing `_type`** via `process_type`.
3. **Processing `_default`** via `process_default_for_constant` — note that
   it receives exactly what step 2 returned as `default_type`, not the raw
   `_type` — so the type is always validated before the default is checked
   against it.
4. **Processing `_validate`** via the shared `process_classmethod` pipeline
   (see [README_METHOD_PROCESSING](README_METHOD_PROCESSING.md)). The
   test value for the dry run is `(self.default,)` — so validation is
   already tried out against the default value at class-definition time.
5. **Cache reset** for atomic instance classes (see below).

[▲ Back to Contents](#-contents)

---

## Type processing (`process_type`)

Normalizes `_type` into a single, predictable runtime form — regardless of
whether the user wrote it as a plain type, a modern union, or a tuple of
types.

**Supported input forms:**

| `_type` written as | Recognized as  | Result                                          |
|:-------------------|:---------------|:------------------------------------------------|
| `int`              | atomic type    | returned immediately, unchanged                 |
| `int \| str`       | `UnionType`    | returned unchanged (after checking for `None`)  |
| `(int, str)`       | tuple of types | converted to `UnionType` via `reduce(or_, ...)` |

**Rule against optionality:** `_type` may never contain `NoneType` (neither
directly nor via a union/tuple) — if it does, `process_type` raises
`raise_union_type_contain_none`. The absence of a value is modeled
elsewhere in the system (at the `normalize`/`process_none` level, see
[README_SIMPLE_CONSTANT](../core/README_SIMPLE_CONSTANT.md#normalize)), never
mixed directly into the type definition itself.

**Why unify into `UnionType`:** the rest of the system can then always call
a plain `isinstance(value, compiled_type)` on the type, regardless of
whether it was originally a single type, a union, or a tuple — no branching
on "what was the actual input format" is needed anywhere else in the code.

**Note on tuple input:** unlike `UnionType` (where only the presence of
`None` is checked), a tuple is additionally checked to make sure it isn't
nested (`(int, (str, float))` is invalid — `_type` must be flat) and
doesn't contain a literal `None` as an element.

[▲ Back to Contents](#-contents)

---

## Default processing (`process_default_for_constant`)

```python
def process_default_for_constant(default_type, owner_class):
    raw_default = getattr(owner_class, "_default", UNSET)
    if raw_default is UNSET or not isinstance(raw_default, default_type):
        validate_default_is_defined(raw_default, owner_class)
        validate_default_matches_annotation(raw_default, default_type, owner_class)
    return raw_default
```

A short but important function with two rules: `_default` must **exist**
and must **match the type** computed in `process_type`. The happy path
(`isinstance` matches) returns immediately without calling the validators —
those only run in the error case, to provide precise diagnostics.

Since constants have no internal structure (unlike compositions),
`_default` is the sole source of their default runtime identity — which is
why it's required for constants, while it's forbidden for compositions (see
[README_SIMPLE_OBJECT_METADATA](README_SIMPLE_OBJECT_METADATA.md#the-forbidden-_default)).

[▲ Back to Contents](#-contents)

---

## Processing `_validate`

A full description of how `process_classmethod` (and its internal
verifiers `verify_classmethod`, `verify_params`,
`verify_annotations_and_defaults`, `verify_calculation`) validates and
normalizes `_validate` is in the shared document
[README_METHOD_PROCESSING](README_METHOD_PROCESSING.md) — the same
pipeline is used, unchanged, for `_logic` and `_decompose` on
`SimpleObjectMetadata` as well.

[▲ Back to Contents](#-contents)

---

## Lazy creation of atomic classes

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

The actual runtime classes for atomic instances (both the mutable and
immutable variants) are **not created automatically when the blueprint is
defined** — they're created lazily, on first access to the corresponding
property. `make_atom_class` (defined in
`_core/metadata/instance_builders/atom_class/`) then compiles the concrete
runtime class via `type(...)`.

This lazy approach has a clear rationale: compiling a runtime class is a
relatively expensive operation (building the `class_dict`, slots, the
`__init__` closure...), and not every blueprint ever needs both variants
(mutable and immutable) — so why pay the cost of a compilation that might
never actually be used.

A deeper look at exactly what `make_atom_class` assembles will be in the
follow-up README about instance creation.

➡️ Next: [README_SIMPLE_OBJECT_METADATA](README_SIMPLE_OBJECT_METADATA.md)

[▲ Back to Contents](#-contents)
