# 🧩 `SimpleObjectMetadata` — Metadata compiler for compositions

`SimpleObjectMetadata` inherits from `SimpleConstantMetadata` (and thereby
from `SimpleBaseMetadata` too) and extends it with everything a composition
needs: validating `_inners`, wiring up `_logic`/`_decompose`, deriving the
default value, and lazily creating composite instance classes.

```
SimpleBaseMetadata
└── SimpleConstantMetadata
    └── SimpleObjectMetadata   ← you are here
```

Because it's a subclass of `SimpleConstantMetadata`, it automatically
inherits fields like `value_type`/`value_type_name` and the `_validate`
processing mechanism too — see
[README_SIMPLE_CONSTANT_METADATA](README_SIMPLE_CONSTANT_METADATA.md).
This document only covers what `SimpleObjectMetadata` adds on top of that.

---

## 🧭 Contents

* [`_process_user_data` — initialization pipeline](#_process_user_data--initialization-pipeline)
* [The forbidden `_default`](#the-forbidden-_default)
* [Processing inner elements (`process_inners`)](#processing-inner-elements-process_inners)
* [Name collisions](#name-collisions)
* [Building the lookup maps](#building-the-lookup-maps)
* [Processing `_logic` and deriving the default](#processing-_logic-and-deriving-the-default)
* [Processing `_decompose` and decomposability](#processing-_decompose-and-decomposability)
* [Lazy creation of composite classes](#lazy-creation-of-composite-classes)

[⬅️ Back to main README](../../README.md)

---

## `_process_user_data` — initialization pipeline

Eleven steps, again run once when the class is defined:

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

The order of these steps isn't accidental — `_logic` (step 7) needs
`inners_default`/`inners_annotations` from step 6 already prepared,
`_decompose` (step 8) needs `self.default` from step 7 already ready (as
the dry-run test value), and `is_decomposeable` (step 9) needs both of
those ready.

[▲ Back to Contents](#-contents)

---

## The forbidden `_default`

```python
if "_default" in self.owner_class.__dict__:
    raise_default_is_defined_in_composition(self.owner_class)
```

This is the very first domain check, even before type or `_inners`
processing — a composition **must not** define `_default` itself. The
check is deliberately on `self.owner_class.__dict__` (the local namespace
only), not `hasattr` — if it checked via `hasattr`, it would also hit the
inherited `_default` from `SimpleConstant` (which holds `UNSET` as a
placeholder there) and would block absolutely everything.

**Why this rule is non-negotiable:** a composition's default must always be
derived from `_logic(defaults of _inners)` (see
[README_SIMPLE_OBJECT](../core/README_SIMPLE_OBJECT.md#important-_default-must-not-be-defined)).
A manual `_default` would create two competing sources of truth — one
declared, one computed — with no guarantee they'd agree. The error message
from `raise_default_is_defined_in_composition` also directly advises how
to fix the class: either remove `_default`, or (if the intent was
different) remove `_inners`/`_logic` and turn the class into a plain
constant instead.

[▲ Back to Contents](#-contents)

---

## Processing inner elements (`process_inners`)

**The invariant the whole function relies on:** because of how
`SimpleMeta.__new__` routes classes (`hasattr(cls, "_inners")` decides
between `SimpleObjectMetadata` and `SimpleConstantMetadata`),
`process_inners` never runs at all if `_inners` doesn't exist — so the
function can safely go straight to `getattr(owner_class, "_inners")`
without a fallback to `UNSET`.

**Optimization: only validate locally declared `_inners`.**
```python
need_validations = "_inners" in owner_class.__dict__
```
If the class merely inherited `_inners` (didn't redefine it itself),
validation is skipped — it was already checked once on the parent class,
and there's no point doing it again. This pattern (`need_validations`
based on local key presence) recurs throughout the metadata system, see
also
[`verify_classmethod`](README_METHOD_PROCESSING.md#verify_classmethod--the-gate-validate-clone-or-inherit).

**Validations that run (only when `need_validations`):**
* `_inners` must be a `tuple` and must not be empty,
* every element must be a class, must inherit from `SimpleConstant`, and
  must not be `SimpleConstant`/`SimpleObject` themselves (only concrete
  subclasses are allowed).

[▲ Back to Contents](#-contents)

---

## Name collisions

The system guarantees **globally unique names across the whole composition
tree** — two different inner elements (even at different nesting levels)
may never share the same `name_snake`. The mechanism:

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

The set intersection (`&`) between what's already registered and the
namespace of the newly added `inner` (`inner.meta.node_names_set` — which
includes all names *nested inside* that inner, not just its own name)
immediately catches a collision at any depth. Two kinds of collision are
distinguished: with the owner itself
(`validate_if_collision_with_owner_class`), and between sibling `_inners`
(`validate_collision_within_inners`).

**The namespace propagates incrementally** — `new_node_names_set` is a copy
of the parent set (`node_names_set.copy()`, to avoid "contaminating"
sibling subtrees), and it's updated (`update`) after each processed
`inner`, so every subsequent `inner` in the same iteration already sees the
names of all the previous ones.

[▲ Back to Contents](#-contents)

---

## Building the lookup maps

```python
self.inners_map = {inner.meta.name_snake: inner for inner in self.inners}
self.inners_params_name = tuple(inner.meta.name_snake for inner in self.inners)
```

These two structures are what `_process_calculate_value_params` uses when
`calculate_value` is called (see
[README_SIMPLE_OBJECT](../core/README_SIMPLE_OBJECT.md#calculate_value)) —
`inners_map` for mapping name → class (validation, defaults),
`inners_params_name` for deriving `_logic`'s expected signature.

[▲ Back to Contents](#-contents)

---

## Processing `_logic` and deriving the default

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

`_logic`'s expected signature is **built dynamically** from `_inners` —
`expected_params` is `("cls",)` plus the name of every inner element, in
the same order. Thanks to `return_calculated_value=True`,
`process_classmethod` returns a `(method, value)` pair — and `self.default`
is exactly the result of the dry run using all `_inners`' default values.
This is the concrete spot in the code where the rule mentioned above holds
true: *a composition's default = `_logic(defaults of _inners)`*, computed
once at class-definition time and fixed from then on.

A full description of how `process_classmethod` itself verifies the method
(signature checks, annotations, dry run) is in
[README_METHOD_PROCESSING](README_METHOD_PROCESSING.md).

[▲ Back to Contents](#-contents)

---

## Processing `_decompose` and decomposability

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

`_decompose` is optional — if the user doesn't define it,
`process_classmethod` (via `verify_classmethod`, see
[README_METHOD_PROCESSING](README_METHOD_PROCESSING.md#verify_classmethod--the-gate-validate-clone-or-inherit))
returns `UNSET` without running a dry run.

**`is_decomposeable` is a recursive condition, not just a local check.**
It's not enough for this particular class to define `_decompose` — a
composition is only decomposable if **every single one** of its inner
elements is either a constant (`inner.meta.is_constant`, atoms are
trivially "decomposable" into themselves) or is itself a decomposable
composition (`inner.meta.is_decomposeable`). In other words: the chain of
decomposability has to run all the way through the whole tree, otherwise
decomposing back would "get stuck" at the lowest level.

[▲ Back to Contents](#-contents)

---

## Lazy creation of composite classes

```python
@property
def composite_class_mutable(self):
    if self._composite_class_mutable is UNSET:
        self._composite_class_mutable = make_composite_class(self.owner_class.__metadata__)
    return self._composite_class_mutable
```

The same lazy pattern as `atom_class_mutable`/`atom_class_immutable` in
`SimpleConstantMetadata` — the actual runtime class is compiled (via
`make_composite_class`) only on first access.

A deeper look at exactly what `make_composite_class` assembles (inheriting
from the atomic class, slots for `_inners`, reactive hooks) will be in the
follow-up README about instance creation.

[▲ Back to Contents](#-contents)
