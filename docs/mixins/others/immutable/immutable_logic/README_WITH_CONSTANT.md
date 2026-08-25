# 🔒 `with_constant` — Immutable Update of a Single Constant

This document describes the smallest building block of the entire immutable
update pipeline — a function that safely changes **one** constant on an
immutable instance without mutating it: it creates a **new** instance with
the structure correctly recalculated. `with_constants`, `with_composite`,
and `with_any` are all built on top of `with_constant` (and especially its
utilities).

> **Integration requirement:** instances on which these functions are called
> must inherit from `Snapshot` (provides `_restore_snapshot`) and `NodesDicts`
> (provides `_nodes_dict`, `_nodes_tuple`...). Without them, the pipeline
> will fail with an `AttributeError`.

```
with_constant
├── create_snapshot_dict     (current state → flat dict)
├── reacalculate_owner_value (recalculate composite parents)
└── create_new_instance      (materialize a new instance)  ← also used independently
```

---

## 🧭 Contents

* [`with_constant` — main pipeline](#with_constant--main-pipeline)
* [`create_snapshot_dict` — flat working copy of the state](#create_snapshot_dict--flat-working-copy-of-the-state)
* [`reacalculate_owner_value` — recalculation toward the root](#reacalculate_owner_value--recalculation-toward-the-root)
* [`create_new_instance` — materialization (used independently)](#create_new_instance--materialization-used-independently)

[⬅️ Back to Immutable methods](../README_IMMUTABLE_METHODS.md#with_constant)

---

## `with_constant` — main pipeline

**Parameters:** `self` (instance with `Snapshot`+`NodesDicts`), `name`
(constant name), `new_value`.

**Return value:** a new instance with the changed value.

**Seven steps:**

```python
def with_constant(self, name, new_value):
    if name not in self._constant_names_set:
        raise_immutability_constant_not_found(self, name)

    instance, path = self._nodes_dict[name]
    instance.validate(new_value)

    snapshot_dict = create_snapshot_dict(self._nodes_tuple)
    snapshot_dict[name] = new_value

    reacalculate_owner_value(snapshot_dict, instance.owner)

    new_snapshot = tuple(snapshot_dict.values())
    return create_new_instance(self, new_snapshot)
```

**Why `name` must be a constant, not an arbitrary node.** The
`name not in self._constant_names_set` check at the very beginning ensures
that `with_constant` cannot accidentally target a composite node — that is
handled by [`with_composite`](README_WITH_COMPOSITE.md), which additionally
has to propagate the change **downward** into its inner elements (something
`with_constant` does not need to handle because a constant has no inner
elements).

**Validation takes place before anything is written** — `instance.validate(new_value)`
is the second step, before the snapshot dictionary is even created. An
invalid value is therefore detected without starting to build any
intermediate state.

**The seven steps correspond exactly to the sequence "check → write →
recalculate → materialize"**: identify the target (`_nodes_dict[name]`),
validate it, create a flat working copy (`create_snapshot_dict`), write the
new value into the copy, recalculate the parents (`reacalculate_owner_value`),
build the final positional tuple, and finally construct a new instance from
it (`create_new_instance`). This five-part pattern — "take snapshot →
modify dict → recalculate → tuple → new instance" — is repeated in nearly
all other `with_*` functions in almost exactly the same way. The only
difference is **what exactly** is written into the dictionary and how
complex the recalculation is.

[▲ Back to top](#-contents)

---

## `create_snapshot_dict` — flat working copy of the state

**Parameters:** `nodes_tuple` (from the `NodesTuple` mixin, see
[NodesTuple design notes](#note-on-nodestuple-nodesdicts-snapshot) below).

**Return value:** `dict[str, Any]` — `{name_snake: _value}`.

```python
def create_snapshot_dict(nodes_tuple):
    return {
        instance.meta.name_snake: instance._value
        for instance, _ in nodes_tuple
    }
```

**Why a `dict` when the `Snapshot` mixin uses a tuple?**
`Snapshot._build_snapshot()` (see `Snapshot.py`) returns positional `tuple`
values — compact, but inconvenient for **targeted** modifications (you want
to change one specific value by name, rather than manually recalculating its
position in the tuple).
`create_snapshot_dict` is the bridge between the two worlds: it converts
`_nodes_tuple` into a dict keyed by `name_snake`, which can easily be mutated
at one specific key. At the end of the pipeline
(`tuple(snapshot_dict.values())`), it is converted back into a positional
tuple — because `_restore_snapshot` (called inside `create_new_instance`)
expects exactly this format.

**It is purely a working intermediate state, not a persistent structure** —
it is created at the beginning of the pipeline, mutated during its execution,
and discarded at the end (after the final `tuple(...)` has been extracted
from it).

[▲ Back to top](#-contents)

---

## `reacalculate_owner_value` — recalculation toward the root

**Parameters:** `snapshot_dict` (mutated in place), `owner` (the instance
from which recalculation starts — typically the direct parent of the changed
node).

**Return value:** `None` — mutates `snapshot_dict` in place.

```python
def reacalculate_owner_value(snapshot_dict, owner):
    current_owner = owner
    while current_owner is not UNSET:
        owner_inners_name = (inner.meta.name_snake for inner in current_owner.meta.inners)
        owner_inners_value_dict = {name: snapshot_dict[name] for name in owner_inners_name}

        new_value = current_owner.meta.logic(**owner_inners_value_dict)
        snapshot_dict[current_owner.meta.name_snake] = new_value

        current_owner = current_owner.owner
```

**Iterative traversal along the `_owner` chain, not recursion.**
`while current_owner is not UNSET` progressively moves from the immediate
parent up to the root of the entire tree — `UNSET` is the value of `_owner`
on the root instance (see
[README_ATOM_CLASS](../../../../metadata/instance/README_ATOM_CLASS.md)),
so the loop naturally terminates once it reaches the top.

**Direct call to `current_owner.meta.logic(...)`, not `calculate_value`.**
Notice that the process does **not** go through the public
`calculate_value` (compare with
[README_SIMPLE_OBJECT](../../../../core/README_SIMPLE_OBJECT.md)) — the raw
`_logic` function from the metadata is called directly. The design notes
justify this explicitly: the values in `snapshot_dict` have **already been
validated** (they either passed `instance.validate(new_value)` in
`with_constant`, or are simply unchanged, previously valid values), so
validating and processing them again through `_process_calculate_value_params`
would be unnecessary. This is a deliberate optimization for an internal,
trusted data path.

**This is the only direction of reactivity that the immutable pipeline needs
to handle manually.** Mutable instances do this automatically through
`_recalculate_self` (see
[README_COMPOSITE_CLASS](../../../../metadata/instance/README_COMPOSITE_CLASS.md))
as a side effect of writing to a slot. Immutable instances, however, do not
allow such writes (see
[README_VALUE_PROPERTIES](../../../../metadata/instance/README_VALUE_PROPERTIES.md)) —
therefore `reacalculate_owner_value` must perform the same work **manually,
in advance**, before a new instance is even created. It performs exactly
the same work that the reactive mechanism would otherwise perform at runtime.

[▲ Back to top](#-contents)

---

## `create_new_instance` — materialization (used independently)

**Parameters:** `instance` (template — used to obtain the class),
`snapshot` (positional tuple of values).

**Return value:** a new, fully initialized instance of the same class.

```python
def create_new_instance(instance, snapshot):
    new_instance = object.__new__(type(instance))
    new_instance.__init__()
    new_instance._restore_snapshot(snapshot)
    return new_instance
```

**Three steps, each with a clear purpose:**

1. **`object.__new__(type(instance))`** — completely bypasses
   `SimpleMeta.__call__`, in exactly the same way as you know from
   [`create_composite_init`](../../../../metadata/instance/README_COMPOSITE_CLASS.md) —
   `type(instance)` is already a finished, compiled runtime class
   (`_is_instance_class = True`), not a blueprint, so going through the
   metaclass would be unnecessary and incorrect.
2. **`new_instance.__init__()`** — runs the **entire** standard
   initialization sequence (slots, `init_mixins`, and, for composites,
   creation of inner elements). The new instance is therefore created just
   as "complete" as any other instance, only with its default values for now.
3. **`_restore_snapshot(snapshot)`** — only now is the actual state from the
   snapshot "injected" into it (the method comes from the `Snapshot` mixin) —
   directly writing to `instance._value` on every node, bypassing the normal
   setter/validation because the values in `snapshot` are already trusted
   (they either passed validation earlier in the pipeline or are unchanged,
   previously valid values).

**Why this function has the "special position" you mentioned.** Although it
was originally created as a helper for `with_constant`, it is general enough
(template + snapshot → fully constructed instance) that it is also called
**directly** by `with_constants`, `with_composite`, and `with_any` (see
[README_WITH_ANY](README_WITH_ANY.md)) — always as the **final step** of
their own pipelines, regardless of how complex the path to the final
`snapshot` tuple was. It is the only place in the entire immutable subsystem
where a new instance is actually created — everything else merely prepares
the data for this one moment.

[▲ Back to top](#-contents)

➡️ Continued in: [README_WITH_CONSTANTS](README_WITH_CONSTANTS.md)
