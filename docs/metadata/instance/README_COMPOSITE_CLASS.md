# 🧩 Composite instance — `make_composite_class` and the reactive core

A composite instance builds directly on the atomic one (see
[README_ATOM_CLASS](README_ATOM_CLASS.md)) — it inherits from it, not from
`InstanceBase` again. This document describes how a composition is
assembled and how the bidirectional reactivity mentioned in the library's
introductory concept actually works.

```
InstanceBase
└── {Meta.owner_class}AtomBase           (atomic base)
    └── {Meta.owner_class}CompositeBase  ← created by make_composite_class
```

---

## 🧭 Contents

* [make_composite_class — compiling the composite class](#make_composite_class--compiling-the-composite-class)
* [_get_inner_instance_class — selecting the class for an inner element](#_get_inner_instance_class--selecting-the-class-for-an-inner-element)
* [create_composite_init — the constructor](#create_composite_init--the-constructor)
* [create_properties_for_inners — accessing inner elements](#create_properties_for_inners--accessing-inner-elements)
* [create_recalculate_self — value flow upward](#create_recalculate_self--value-flow-upward)
* [create_recalculate_inners — value flow downward](#create_recalculate_inners--value-flow-downward)
* [Reactivity as a whole](#reactivity-as-a-whole)

[⬅️ Back to main README](../../../README.md)

---

## `make_composite_class` — compiling the composite class

**Parameters:** `meta`, `mutable` (default `True`).

**Return value:** a dynamically created class (`CompositeInstanceProtocol`).

**Under the hood (abridged):**
```python
def make_composite_class(meta, *, mutable=True):
    base_class_name = f"{meta.class_name}Composite{'Mutable' if mutable else 'Immutable'}Base"
    base_class = meta.atom_class_mutable if mutable else meta.atom_class_immutable
    class_parents = (base_class,)

    class_dict = {
        "__metadata__": meta,
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name, mutable=mutable),
        "value": create_value_property(meta, is_constant=False, mutable=mutable),
    }
    class_dict |= create_properties_for_inners(meta, mutable=mutable)

    if mutable:
        class_dict["_recalculate_self"] = create_recalculate_self(meta, base_class_name)
        class_dict["_recalculate_inners"] = create_recalculate_inners(meta, base_class_name)

    composite_class = type(base_class_name, class_parents, class_dict)

    return composite_class
```

**A single parent — the atomic class.** `class_parents = (base_class,)`,
where `base_class` is precisely the already-compiled
`atom_class_mutable`/`_immutable`. So a composition **is** an atom (it
inherits `_value`, `_owner`, `_locked`, `_root_value_setter`,
`init_mixins`, `meta`...) and adds its own structure on top. This is
exactly the mechanism that lets a composition have its own `value`
(overridden below with composite behavior) while staying compatible with
everything that relies on the atomic interface (e.g. `_root_value_setter`
called from the parent's `_recalculate_inners`).

**Slots are derived directly from `_inners`** —
`tuple(inner.meta.name_private for inner in meta.inners)` — each inner
element gets its own private slot (e.g. `_engine`, `_wheels`), which
stores its **instance** (not the value — the instance).

**Reactive hooks only for mutable.** `_recalculate_self` and
`_recalculate_inners` (below) only make sense where values can actually
change at all — an immutable composition is structurally frozen once
initialized.

**The same note on declarative attributes applies here as for atoms** (see
[README_ATOM_CLASS](README_ATOM_CLASS.md#make_atom_class--compiling-the-atomic-class))
— `inners`, `_logic`, and `_decompose` are never placed into `class_dict`,
so they never appear in `composite_class`'s own `__dict__`, but they
remain reachable through the MRO via the atom base class /
`meta.owner_class`.

[▲ Back to Contents](#-contents)

---

## `_get_inner_instance_class` — selecting the class for an inner element

**Parameters:** `inner_meta`, `mutable`.

**Return value:** the correct instance class for the given inner element.

**Under the hood:**
```python
def _get_inner_instance_class(inner_meta, mutable):
    if mutable:
        return inner_meta.atom_class_mutable if inner_meta.is_constant else inner_meta.composite_class_mutable
    return inner_meta.atom_class_immutable if inner_meta.is_constant else inner_meta.composite_class_immutable
```

A small but important 2×2 decision matrix (mutable/immutable ×
constant/composite) — an inner element of a composition can itself be
either an atom or another composition (recursive nesting to any depth),
and this function makes sure the correct one of the four variants is
picked for it. Accessing it via `inner_meta.atom_class_mutable` etc. also
**triggers lazy creation** of that class if it doesn't exist yet (see
[README_SIMPLE_CONSTANT_METADATA](../README_SIMPLE_CONSTANT_METADATA.md))
— so even deeply nested composition trees compile efficiently, only on
demand.

[▲ Back to Contents](#-contents)

---

## `create_composite_init` — the constructor

**Parameters:** `meta`, `base_class_name`, `mutable` (default `True`).

**Return value:** the `__init__` function as a closure.

**Under the hood:**
```python
def create_composite_init(meta, base_class_name, *, mutable=True):
    def __init__(self):
        for inner in meta.inners:
            inner_meta = inner.meta
            inner_cls = _get_inner_instance_class(inner_meta, mutable)
            inner_instance = object.__new__(inner_cls)
            inner_instance.__init__()
            inner_instance._owner = self
            setattr(self, inner_meta.name_private, inner_instance)

        if mutable:
            meta.atom_class_mutable.__init__(self)
        else:
            meta.atom_class_immutable.__init__(self)

    ...
    return __init__
```

**A strictly fixed order of steps — and it's not accidental.** First
**all** inner elements are created and wired up, and only then is the
atomic layer's initialization called
(`meta.atom_class_mutable.__init__(self)`, which among other things runs
`init_mixins`). Reason: mixins initialized during the atomic phase
(typically structural ones, like `NodesTuple`/`NodesDicts` — see the
mixins section) expect the tree of inner elements to be **already
complete** by the time they run. If the order were reversed, these mixins
would run into missing slots.

**Creating inner instances deliberately bypasses `SimpleMeta.__call__`
entirely** — `object.__new__(inner_cls)` plus a manual
`inner_instance.__init__()` instead of simply calling `inner_cls()`. If
`inner_cls()` were called, it would go through the metaclass (since
`inner_cls` is still a class with `SimpleMeta`), and `SimpleMeta.__call__`
would run the **entire** `create_instance` pipeline again — needlessly and
incorrectly, since `inner_cls` is already a finished, compiled runtime
class, not a blueprint.

**The `_owner` link is a bidirectional relationship** —
`inner_instance._owner = self` gives the inner element a reference to its
parent, which is exactly what `_root_value_setter` needs for bubbling
changes upward (see
[README_ATOM_CLASS](README_ATOM_CLASS.md)).

**No `super()`.** The comment in the `_DESIGN_NOTES` source explains this
clearly: an explicit call
(`meta.atom_class_mutable.__init__(self)`) is deterministic and independent
of the MRO, whereas `super()` could lead to an unclear call order in a
dynamically assembled class hierarchy.

[▲ Back to Contents](#-contents)

---

## `create_properties_for_inners` — accessing inner elements

**Parameters:** `meta`, `mutable` (default `True`).

**Return value:** a `dict` — properties to be merged into `class_dict`.

**Under the hood:**
```python
def create_properties_for_inners(meta, *, mutable=True):
    return {
        k: v
        for inner in meta.inners
        for k, v in create_properties_for_inner(inner.meta, path=(), mutable=mutable).items()
    }
```

For every direct inner element, this generates **two** properties (a
detailed description of the mechanics is in
[README_VALUE_PROPERTIES](README_VALUE_PROPERTIES.md)): `<name>` for
accessing the value, and `<name>_instance` for accessing the instance
itself. The result is merged into `class_dict` via `|=` — so the
properties are created **at class-compilation time**, not at runtime
through a `setattr` loop, which is faster and allows static introspection
(`dir(instance)` shows every property right away).

[▲ Back to Contents](#-contents)

---

## `create_recalculate_self` — value flow upward

**Parameters:** `meta`, `base_class_name`.

**Return value:** the `_recalculate_self` function as a closure. Only for
mutable variants.

**Under the hood:**
```python
def create_recalculate_self(meta, base_class_name):
    def _recalculate_self(self):
        current_values = {
            inner.meta.name_snake: getattr(self, inner.meta.name_private).value
            for inner in meta.inners
        }
        new_value = self.calculate_value(**current_values)

        try:
            if self._value == new_value:
                return
        except Exception:
            pass

        self._value = new_value

        if self._owner:
            self._owner._recalculate_self()

    ...
    return _recalculate_self
```

This answers the question "what happens when a value **inside** the
composition changes" (🔼 from the introductory concept):

1. **Collect the current values of all direct children** into a
   `{name: value}` map — exactly the format `calculate_value` (or rather
   `_process_calculate_value_params`) expects as kwargs.
2. **Recalculate** — the public `self.calculate_value(**current_values)` is
   called, the very same method a user would call by hand (see
   [README_SIMPLE_OBJECT](../../core/README_SIMPLE_OBJECT.md)).
3. **Short-circuit on a match** — the same pattern as in
   `_root_value_setter`, here additionally wrapped in `try/except`, since
   comparison (`==`) isn't necessarily safe for an arbitrary type.
4. **Write and bubble further upward** — if the value changed, it's stored
   and (if an owner exists) `_recalculate_self` is called on **this
   composition's parent** — the chain runs all the way up to the topmost
   root of the tree.

[▲ Back to Contents](#-contents)

---

## `create_recalculate_inners` — value flow downward

**Parameters:** `meta`, `base_class_name`.

**Return value:** the `_recalculate_inners` function as a closure. Only
for mutable variants.

**Under the hood:**
```python
def create_recalculate_inners(meta, base_class_name):
    def _recalculate_inners(self):
        decomposed = self.decompose_value(self._value)

        for inner, inner_value in zip(meta.inners, decomposed):
            inner_instance = getattr(self, inner.meta.name_private)
            inner_instance._root_value_setter(inner_value, recalculate_up=False)

            if not inner.meta.is_constant:
                inner_instance._recalculate_inners()

    ...
    return _recalculate_inners
```

The reverse direction (🔽 from the introductory concept) — "what happens
when the value of the **whole** composition changes":

1. **Decompose** — `self.decompose_value(self._value)` breaks the current
   value into pieces for the individual `_inners` (see
   [README_SIMPLE_OBJECT](../../core/README_SIMPLE_OBJECT.md)).
2. **Distribute the pieces to the children** — for each inner element, its
   `_root_value_setter` is called with **`recalculate_up=False`** — this
   is crucial: without it, writing to a child would immediately trigger
   `_recalculate_self` back on the parent, creating an infinite loop
   (down → up → down → ...).
3. **Cascade into nested compositions** — if the inner element is itself
   another composition (`not inner.meta.is_constant`), its own
   `_recalculate_inners()` is called recursively, so the decomposition
   propagates to any depth of the tree.

**`zip(meta.inners, decomposed)` enforces a strict positional match** —
which is why `verify_decompose_outcome` (see
[README_METHOD_PROCESSING](../README_METHOD_PROCESSING.md)) checks that
`_decompose` returns a tuple of exactly the same length and order as
`_inners`.

[▲ Back to Contents](#-contents)

---

## Reactivity as a whole

The two reactive methods together form a closed, safe cycle:

```
write to an inner element (_root_value_setter, recalculate_up=True)
        │
        ▼
  _recalculate_self  (on the parent, may bubble further upward)
        │
write to the composition (value = ..., via create_value_setter)
        │
        ▼
  _recalculate_inners  (distributes to children with recalculate_up=False)
```

The key safety mechanism against infinite loops is always the same: **the
direction a change is currently propagating in carries
`recalculate_up=False`**, so it can never "bounce back". Combined with the
short-circuit checks (value didn't change → no further propagation), this
also guarantees that even a large composition tree reacts to a single
change with only the minimum necessary number of recalculations.

➡️ Next: [README_CREATE_INSTANCE](README_CREATE_INSTANCE.md)

[▲ Back to Contents](#-contents)
