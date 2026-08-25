# 📋 Instance protocols — What an instance can do out of the box

This document is a reference overview of what a **freshly created instance
has available, before a single mixin is attached to it**. It's the "empty
table" — the base interface that mixins then build additional capabilities
on top of (see the Mixins section).

There are four variants, along two independent axes described in
[README_CREATE_INSTANCE](README_CREATE_INSTANCE.md):

|  | **Mutable** | **Immutable** |
|---|---|---|
| **Atomic** (`SimpleConstant`) | [Atomic mutable](#1-atomic-mutable-instance) | [Atomic immutable](#2-atomic-immutable-instance) |
| **Composite** (`SimpleObject`) | [Composite mutable](#3-composite-mutable-instance) | [Composite immutable](#4-composite-immutable-instance) |

The composite variants **inherit everything** from the corresponding
atomic variant (mutable from mutable, immutable from immutable) — see
[README_COMPOSITE_CLASS](README_COMPOSITE_CLASS.md) — so this isn't
repeated in the tables below, only referenced.

---

## 🧭 Contents

* [1. Atomic mutable instance](#1-atomic-mutable-instance)
* [2. Atomic immutable instance](#2-atomic-immutable-instance)
* [3. Composite mutable instance](#3-composite-mutable-instance)
* [4. Composite immutable instance](#4-composite-immutable-instance)

[⬅️ Back to main README](../../../README.md)

---

## 1. Atomic mutable instance

Created by calling `MyConstant()` (the default — `mutable=True`).

### Slots (internal state)

| Slot | Description |
|---|---|
| `_value` | The current normalized value. |
| `_owner` | A reference to the parent composition, if this atom is one of its inner elements. Otherwise `UNSET`. |
| `_locked` | The lock flag (`False` on a fresh instance). |
| `__weakref__` | Weak-reference support (from `InstanceBase`). |

### Public interface

| Member | Type | Description |
|---|---|---|
| `value` | property (read/write) | The main way to access the value. Writing normalizes, stores, and triggers bubbling upward if the instance has an owner. |
| `owner` | property (read-only) | Returns `_owner`. |
| `meta` | property (read-only) | The blueprint's metadata that the instance was created from (`SimpleConstantMetadata`). |
| `init_mixins()` | method | An empty hook (does nothing without mixins). |
| `validate_type(value, ...)` | classmethod\* | Inherited from the blueprint — deterministic type validation. |
| `validate(value, ...)` | classmethod\* | Inherited from the blueprint — full validation (type + `_validate`). |
| `is_valid(value)` | classmethod\* | Inherited from the blueprint — the boolean variant of `validate`. |
| `normalize(value, ...)` | classmethod\* | Inherited from the blueprint — input normalization. |
| `__repr__()` | method | A diagnostic dump: class name, blueprint path, current value, memory address. |
| `__str__()` | method | The class name. |

\* These methods are **inherited directly from the user's blueprint
class** (`meta.owner_class`), because `make_atom_class` builds the
instance on dual inheritance, `(InstanceBase, meta.owner_class)` — see
[README_ATOM_CLASS](README_ATOM_CLASS.md). They work exactly as if called
directly on the blueprint — it's just that now a specific instance is
calling them.

### The blueprint's declarative attributes

`_type`, `_default`, `_validate` (as an overridable hook — validation
itself remains available via `validate`/`is_valid`), and
`bool_or_raise_validate_error` are not part of the instance's own
compiled namespace, but they **do** remain reachable on the instance
through the MRO, since `meta.owner_class` (the user's blueprint) is one of
its parents (see
[README_ATOM_CLASS](README_ATOM_CLASS.md#make_atom_class--compiling-the-atomic-class)).

[▲ Back to Contents](#-contents)

---

## 2. Atomic immutable instance

Created by calling `MyConstant(mutable=False)`. Requires the `_type`
value to be hashable (checked in `create_instance`).

### Differences from the mutable variant

| Member | Difference |
|---|---|
| `value` | The property has **only a getter**. Attempting to write (`instance.value = ...`) fails with `AttributeError` already at the Python level — the setter is never even created for the immutable variant. |
| `_root_value_setter` | **Doesn't exist.** This method is only added to `class_dict` conditionally, `if mutable` (see [README_ATOM_CLASS](README_ATOM_CLASS.md#create_root_value_setter--reactive-value-writes)). |

Everything else (slots, `owner`, `meta`, the validation methods,
`__repr__`/`__str__`) is the same as in the mutable variant.

[▲ Back to Contents](#-contents)

---

## 3. Composite mutable instance

Created by calling `MyObject()`. Inherits **everything** from the
[atomic mutable instance](#1-atomic-mutable-instance) — the
`_value`/`_owner`/`_locked` slots, `owner`, `meta`, the validation
methods, `__repr__`/`__str__`. The table below shows only what it adds on
top.

### Extra slots

One private slot for **every direct inner element** declared in
`_inners` — e.g. for `_inners = (Engine, Wheels)`, the slots `_engine`
and `_wheels` are created, each holding an instance of the given inner
element.

### Extra public interface

| Member | Type | Description |
|---|---|---|
| `value` | property (read/write, **overridden**) | The getter follows the same principle as on the atom. The setter additionally requires `meta.is_decomposeable`, and after writing it automatically distributes the new value to the inner elements (`_recalculate_inners`). |
| `<inner_name>` | property (read/write*) | For every direct inner element — direct access to its value, e.g. `instance.engine`. Writing follows the same rules as `value` for that particular element (atomic/composite, depending on its own nature). |
| `<inner_name>_instance` | property (read-only) | Access to the inner element's instance itself, not its value, e.g. `instance.engine_instance`. |
| `calculate_value(*args, **kwargs)` | classmethod\* | Inherited from the blueprint — computes the value from parameters matching `_inners`. |
| `decompose_value(value)` | classmethod\* | Inherited from the blueprint — decomposes a value back into pieces for `_inners` (only if `is_decomposeable`). |
| `_recalculate_self()` | method (internal) | Recalculates its own value from the children's current values and bubbles upward. |
| `_recalculate_inners()` | method (internal) | Decomposes its own value and distributes the pieces to the children. |

\* Same as with the atom — inherited from the user's blueprint class.

> **Note on `<inner_name>` properties:** the exact list varies by class —
> it depends on what's declared in `_inners`. This table describes the
> *mechanism* (that every inner element gets a value/instance-property
> pair), not the concrete names, which are always specific to the given
> composition.

[▲ Back to Contents](#-contents)

---

## 4. Composite immutable instance

Created by calling `MyObject(mutable=False)`. Inherits **everything**
from the [atomic immutable instance](#2-atomic-immutable-instance) plus
the structure from the [composite mutable variant](#3-composite-mutable-instance),
minus the reactive write mechanisms.

### Differences from the composite mutable variant

| Member | Difference |
|---|---|
| `value` | Getter only — same as with the atomic immutable variant. |
| `<inner_name>` | Getter only — writing to any inner element is not allowed. |
| `_recalculate_self` | **Doesn't exist.** Only added to `class_dict` conditionally, `if mutable`. |
| `_recalculate_inners` | **Doesn't exist.** Same reason. |

`<inner_name>_instance` remains (it's always read-only regardless of
mutability), and `calculate_value`/`decompose_value` remain available as
inherited methods — they're just computation/decomposition, not a
mutation of the instance's state.

An immutable composition is therefore **structurally frozen** once
created — the value can be read at any level of the tree, but it can't be
changed anywhere.

[▲ Back to Contents](#-contents)
