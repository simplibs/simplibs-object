# 🔒 `with_constants` — Batch Immutable Update of Constants

The batch variant of [`with_constant`](README_WITH_CONSTANT.md) — instead
of changing one constant at a time, it can safely change **any number of**
constants in a single operation, with **one** final structure recalculation
instead of recalculating the structure after each individual change.

> The same integration requirement as for `with_constant`: the instance must
> inherit from `Snapshot` and `NodesDicts`.

```text
with_constants
├── create_snapshot_dict     (from with_constant/utils, shared)
├── find_longest_keys        (finds the "deepest" changed nodes)
├── reacalculate_owner_value (started from each deepest node)
└── create_new_instance      (shared with with_constant)
```

---

## 🧭 Contents

* [`with_constants` — main pipeline](#with_constants--main-pipeline)
* [`find_longest_keys` — why it is needed](#find_longest_keys--why-it-is-needed)

[⬅️ Back to Immutable methods](../README_IMMUTABLE_METHODS.md#with_constants)

---

## `with_constants` — main pipeline

**Parameters:** `self`, `changes` (`ChangeTuple | ChangesTuple | None`) —
either a single `(name, value)` pair or a tuple of such pairs.

**Return value:** a new instance with all changes applied at once.

**Six steps:**

```text
1. snapshot_dict = create_snapshot_dict(self._nodes_tuple)
2. path_dict = {}
3. new_snapshot = self._build_snapshot()   ← fallback if changes is empty

4. (only if changes exist)
   4.1 changes MUST be a tuple
   4.2 normalization: a single pair (name, value) → wrapped in a tuple of pairs
   4.3 for each (name, value):
       - validate the pair structure
       - name MUST be in self._constant_names_set
       - validate the value through instance.validate
       - write the value to snapshot_dict
       - write the path to path_dict
   4.4 longest_key = find_longest_keys(path_dict)
   4.5 for each key in longest_key: reacalculate_owner_value(...)
   4.6 new_snapshot = tuple(snapshot_dict.values())

5. return create_new_instance(self, new_snapshot)
```

**Normalization of a single pair into a tuple of pairs** (step 4.2,
`if not isinstance(changes[0], tuple): changes = (changes,)`) — the same
convenience pattern as `assert_mixins_slots_values`:
`with_constants(self, ("age", 25))` and `with_constants(self, (("age", 25),))` 
behave identically, so the user does not have to write an
unnecessarily nested tuple for a single change.

**The key difference compared to repeated calls to `with_constant`** is in
the **recalculation phase** (steps 4.4–4.5). If you called `with_constant`
ten times in a row instead of using `with_constants`, each call would
independently recalculate the entire path to the root — with shared parents,
this would mean **repeated, unnecessary work** (the same composite node
would be recalculated multiple times). `with_constants` avoids this by
first **collecting all changes** into a single `snapshot_dict`, and only
then performing the recalculation — starting only from the **deepest**
changed locations (see `find_longest_keys` below). This ensures that every
shared parent is recalculated **exactly once**, regardless of how many of its
descendants have changed.

[▲ Back to top](#-contents)

---

## `find_longest_keys` — why it is needed

**Parameters:** `path_dict` (`{name: path}` for each changed constant).

**Return value:** `tuple[str, ...]` — the names of only those constants whose
paths are "terminal" (deepest) among the supplied changes.

```python
def find_longest_keys(path_dict):
    sorted_path = sorted(path_dict.items(), key=lambda x: x[1])
    longest_keys = []

    for i in range(len(sorted_path) - 1):
        key, path = sorted_path[i]
        _, next_path = sorted_path[i + 1]
        if next_path[:len(path)] == path:
            continue  # path is a prefix of next_path → NOT terminal
        longest_keys.append(key)

    longest_keys.append(sorted_path[-1][0])  # last one is always terminal
    return tuple(longest_keys)
```

**Why it would be wrong to start the recalculation directly from all changed
nodes.** Imagine a `Car` composite containing an `Engine`, which in turn
contains a `Cylinder`. If the user changes both `cylinder_count` and
`engine_power` (where `engine_power` is *directly* on `Engine`, not on
`Cylinder`), both paths lead to the same parent (`Engine`) — if
`reacalculate_owner_value` were started independently from **both** points,
`Engine` (and `Car` above it) would be recalculated **twice**.
`find_longest_keys` solves this by identifying only those changes that are
actually at the "leaf", deepest level relative to **the other supplied
changes** — and `reacalculate_owner_value` (which already walks all the way
to the root, see
[README_WITH_CONSTANT](README_WITH_CONSTANT.md))
is then started only from these points. This automatically covers all
intermediate levels without calculating them more than once.

**The algorithm is based on sorting paths and testing prefixes, not on
explicit tree comparison.** `sorted(path_dict.items(), key=lambda
x: x[1])` sorts the entries by their path (a tuple of strings, which are
compared lexicographically element by element) — therefore, if path A is a
prefix of path B, A will appear immediately **before** B after sorting (or
somewhere before it within a group of sibling paths sharing the same
prefix). The `next_path[:len(path)] == path` test then simply checks whether
the current path is a **prefix** of the next path in sorted order — if so,
the current path is a "parent" that does **not** need to be included
(its processing would be redundant because its descendant will be processed).
The last element of the sorted list is always included unconditionally,
because no other element can follow it for comparison.

[▲ Back to top](#-contents)

➡️ Continued in: [README_WITH_COMPOSITE](README_WITH_COMPOSITE.md)
