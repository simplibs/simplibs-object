# 🎲 Randomize — Fuzzing with random values

This document describes two tools that connect `simplibs-object` with
`simplibs-randomize` — the
library we documented first, in order. While that library was about
generating random values on their own, here the same library gets plugged
**into the instance tree**, so it can fill an entire composition (or just
a single atom) with valid random data — typically for testing.

Two files, two levels:

* **`randomize_value`** — the low-level "engine": generates and assigns a
  random value to **one specific** leaf instance.
* **`random_data_filler`** — the high-level orchestrator: walks the
  **entire tree** of an instance (a composition and its nested elements)
  and calls `randomize_value` at every suitable spot.

---

## 🧭 Contents

* [`randomize_value` — one leaf](#randomize_value--one-leaf)
* [`random_data_filler` — the whole tree](#random_data_filler--the-whole-tree)
* [How the two functions relate to each other](#how-the-two-functions-relate-to-each-other)

[⬅️ Back to main README](../../README.md)

---

## `randomize_value` — one leaf

**Parameters:**
* `instance` (*SimpleInstanceLike*): the target instance to fill with a
  random value.
* `retries` (*int*): the maximum number of attempts to generate and assign
  a value.
* `registry` (*RegistryBase | None*): an optional custom randomizer
  registry — if `None`, the global `RANDOMIZERS` is used.
* `skip_unregistered` (*bool*, default `False`): if `True`, silently skips
  types with no registered randomizer, instead of raising
  `RandomizeError`.
* `validate` (*bool*, default `True`): toggles input-parameter checking.

**Return value:** the same instance, mutated in place.

**Exceptions:**
* `SimpleRuntimeError` — invalid parameters, or `retries` exhausted.
* `RandomizeError` — the value's type has no registered randomizer and
  `skip_unregistered=False`.

**Under the hood (abridged):**
```python
def randomize_value(instance, *, retries, registry, skip_unregistered=False, validate=True):
    ...
    value_randomizer = registry.randomize if registry else randomize

    for _ in range(retries):
        try:
            value_type = instance.meta.value_type
            new_value = value_randomizer(value_type)
        except RandomizeError:
            if skip_unregistered:
                return instance
            raise

        if new_value == instance.value:
            continue

        try:
            instance.value = new_value
            return instance
        except Exception:
            continue

    raise_random_data_filler_exhausted(instance, retries)
```

**Four layers of robustness in a single loop:**

1. **The registry is swappable** — `registry.randomize if registry else
   randomize` — the function works equally well with the global registry
   or with an isolated `LocalRegistry`, which lets fuzzing be scoped to a
   predictable set of values (e.g. in tests).
2. **An unregistered type can either be ignored or reported** — the
   behavior is controlled by `skip_unregistered`. In the context of a
   composition tree (see `random_data_filler` below), "ignore" typically
   makes sense, since not every type in the system needs to have its own
   randomizer.
3. **Rejecting an identical value** (`if new_value == instance.value:
   continue`) — the function guarantees that the value **actually
   changes**, not just that it "tries" and possibly returns the same one.
4. **Catching validation errors from the setter** (`except Exception:
   continue`) — a generated random value might pass the randomizer's type
   check but still fail the given instance's **domain** validation
   (`_validate`). The setter catches this, and the loop treats it as "try
   again," not as a fatal error — until `retries` runs out.

**Why `raise_random_data_filler_exhausted` at the end, instead of failing
silently** — if a valid, different value still can't be found even after
`retries` attempts, that's a signal that either `retries` is set too low,
or the domain validation is strict enough that random values of that type
almost never pass — either way, it's better to know that immediately
rather than end up with a silently unchanged value.

[▲ Back to Contents](#-contents)

---

## `random_data_filler` — the whole tree

**Parameters:**
* `instance` (*SimpleInstanceLike*): the root of the tree (atom, or
  composition) to fill.
* `retries` (*int*, default `5`): the attempt limit for **each** leaf
  separately.
* `registry` (*RegistryBase | None*, default `None`).
* `skip_unregistered` (*bool*, default `False`).
* `skip_immutable` (*bool*, default `True`): skips locked/immutable
  instances instead of attempting to mutate them.
* `validate` (*bool*, default `True`).

**Return value:** the same root instance, mutated in place (the whole
subtree, not just the root).

**Under the hood (abridged):**
```python
def random_data_filler(instance, *, retries=5, registry=None,
                        skip_unregistered=False, skip_immutable=True, validate=True):
    ...
    is_immutable = not getattr(instance, "__is_mutable__", True)
    is_locked = getattr(instance, "_locked", False)
    if skip_immutable and (is_immutable or is_locked):
        return instance

    if instance.meta.is_constant or instance.meta.is_decomposeable:
        randomize_value(instance, retries=retries, registry=registry,
                         skip_unregistered=skip_unregistered, validate=False)

    if hasattr(instance.meta, "inners"):
        for inner in instance.meta.inners:
            inner_instance = getattr(instance, inner.meta.name_private)
            random_data_filler(inner_instance, retries=retries, registry=registry,
                                skip_unregistered=skip_unregistered,
                                skip_immutable=skip_immutable, validate=False)

    return instance
```

**A recursive tree walk with two independent actions at every node** —
this is the core idea of the whole function:

1. **Direct assignment** (the "top-down" step) — if the node is either an
   atom (`is_constant`) or a decomposable composition
   (`is_decomposeable`), `randomize_value` is called on it directly. For a
   decomposable composition, this means generating a random value for the
   **whole composition at once** and letting `_recalculate_inners` (see
   [README_COMPOSITE_CLASS](../metadata/instance/README_COMPOSITE_CLASS.md#create_recalculate_inners--value-flow-downward))
   distribute it down into the inner elements — which exercises **top-down**
   propagation.
2. **Recursion into children** (the "bottom-up" step) — regardless of
   whether step 1 ran, the function walks `instance.meta.inners` (if any
   exist) and calls itself recursively on every inner element. Since inner
   elements bubble their own random assignment back upward via
   `_recalculate_self`, this also exercises **bottom-up** propagation.

The combination of both steps means `random_data_filler` incidentally also
serves as a **reactive stress test** — a single call of the function at
the root exercises both reactive directions described in
[README_COMPOSITE_CLASS](../metadata/instance/README_COMPOSITE_CLASS.md#reactivity-as-a-whole).

**Protection against mutating a locked/immutable state** is the first
thing checked at every node (`skip_immutable and (is_immutable or
is_locked)`) — thanks to `getattr(..., True)`/`getattr(..., False)` with
safe defaults, the function doesn't crash even if it encounters an
instance without these attributes.

**`validate=False` in every recursive/downstream call** — validation of
the input parameters (the type of `instance`, `retries > 0`...) only runs
once, at the level of the first call made by the user. Every subsequent
call (whether `randomize_value` inside it, or a recursive call to itself)
turns it off — the parameters don't change during recursion, so repeated
validation would be purely unnecessary overhead.

[▲ Back to Contents](#-contents)

---

## How the two functions relate to each other

```
random_data_filler(root)
│
├─ root.meta.is_constant / is_decomposeable?
│    └─ randomize_value(root, ...)          ← generates and assigns 1 value
│
└─ for each root.meta.inners:
     └─ random_data_filler(inner_instance)  ← recursion, same pattern again
```

`randomize_value` never knows anything about the tree structure — it works
with just one instance. `random_data_filler`, on the other hand, never
generates values itself — it delegates all the randomizer work to
`randomize_value` and focuses exclusively on **walking the tree and
deciding where to call what**. This division of responsibilities is the
same pattern seen elsewhere in the library (e.g. `calculate_value` vs.
`_process_calculate_value_params`) — one function handles "what," the
other "where/how often."

[▲ Back to Contents](#-contents)
