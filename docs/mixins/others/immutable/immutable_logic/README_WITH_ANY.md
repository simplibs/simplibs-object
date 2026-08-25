# 🔒 `with_any` — Universal Immutable Update

The highest layer of the immutable update pipeline — a single entry point
capable of handling **any** combination of changes (one constant, one
composite, a batch of constants, a batch of composites, or anything mixed
together). It automatically decides in which order and how to apply them
safely. It builds on all three previous documents —
[`with_constant`](README_WITH_CONSTANT.md),
[`with_constants`](README_WITH_CONSTANTS.md),
[`with_composite`](README_WITH_COMPOSITE.md) — and adds a layer that
intelligently routes between them.

> Same integration requirement as with the previous functions: the
> instance must inherit from `Snapshot` and `NodesDicts`.

```
with_any
├── split_changes            (splits input into constants / composites)
├── get_top_composite_paths  (finds “root” composite changes)
├── with_composite           (applies root composites)
├── split_constants_paths    (splits constants into “contained” / “unique”)
├── with_constants           (applies unique constants)
└── process_single_change    (shortcut for a single change)
```

---

## 🧭 Contents

* [`with_any` — main pipeline](#with_any--main-pipeline)
* [`process_single_change` — shortcut for one change](#process_single_change--shortcut-for-one-change)
* [`split_changes` — constants vs composites](#split_changes--constants-vs-composites)
* [`get_top_composite_paths` — root vs nested composites](#get_top_composite_paths--root-vs-nested-composites)
* [`split_constants_paths` — contained vs unique constants](#split_constants_paths--contained-vs-unique-constants)
* [Why this orchestration is necessary](#why-this-entire-orchestration-is-necessary)

[⬅️ Back to Immutable methods](../README_IMMUTABLE_METHODS.md#with_changes)

---

## `with_any` — main pipeline

**Parameters:** `self`, `changes` (`ChangeTuple | ChangesTuple | None`).

**Return value:** a new instance (immutable mode), or directly the value
(`instance.value`, if `self.__is_mutable__` — see note below).

**Thirteen steps, but they can be grouped into four phases:**

```
PHASE A — trivial paths (steps 1–3)
  1. changes is empty/None → create a copy without modification
  2. changes must be a tuple
  3. a single change (not a tuple of tuples) → delegate to process_single_change

PHASE B — classification (steps 4–7)
  4. split_changes → (constants, composite)
  5. only constants → delegate directly to with_constants
  6. build changes_dict for fast lookup by name
  7. get_top_composite_paths → (top_composite, child_composite)

PHASE C — applying composites top-down (steps 8–11)
  8. create a fresh instance (copy) as the working base
  9. for each name in top_composite: instance = with_composite(instance, name, ...)
  10. extract snapshot_dict from the instance AFTER applying composites
  11. verify that child_composite values match what the composite already set

PHASE D — applying constants (steps 12–13)
  12. split_constants_paths → (contained, unique); verify contained; apply unique
  13. return instance (or instance.value, if self.__is_mutable__)
```

**Phase A: why three different “outputs” for trivial inputs?**  
Steps 1 and 3 are not just optimizations — they represent **different
semantics**. Step 1 (`not changes`) means “no change, just return an
equivalent new instance” (useful as an explicit “clone”). Step 3 (single
change) delegates to the specialized, simpler
[`process_single_change`](#process_single_change--shortcut-for-one-change) —
no need to run the heavy classification machinery of steps 4–13 for a
single item.

**Phase B, step 5 — “only constants” is another shortcut.**  
If `split_changes` determines that none of the changes are composite,
then the rest of the orchestration (phases C and D) is unnecessary —
`with_constants` (see [README_WITH_CONSTANTS](README_WITH_CONSTANTS.md)`)
already efficiently handles a batch of constants, including optimized
recalculation only from the deepest nodes.

**Phase C is the core reason `with_any` exists.**  
Composite changes must be applied **from the root downward**
(`top_composite` first), because applying a root composite (via
`with_composite` → `reacalculate_inners`) **automatically** sets the
values of all its nested elements. If the user also requested a change
on one of those nested elements (`child_composite`), that second change
cannot be applied again — it would be inconsistent (two different paths
to the same value may produce different results). Instead, `child_composite`
changes are **verified** (step 11) against what the root composite
already set — if the user provided a value that **does not match** what
the root composite implies, it triggers
`raise_with_any_child_composite_mismatch`.

**Phase D, step 12 solves the analogous problem for constants.**  
[`split_constants_paths`](#split_constants_paths--contained-vs-unique-constants)
distinguishes constants that **fall inside** an already applied root
composite (these are only verified, not re-applied — same reason as
`child_composite`) from constants that lie **outside** any applied
composite (these are actually applied via `with_constants`).

**`self.__is_mutable__` at the end is intentional — a dual semantic.**  
`with_any` (and the entire immutable subsystem) is often called from
mutable instances (e.g., as an implementation of a public “copy-with”
method) — in that case it makes sense to return the **value**
(`instance.value`) directly, not the immutable instance, because the
caller operates in a mutable context where an immutable instance would be
an alien concept.

[▲ Back to top](#-contents)

---

## `process_single_change` — shortcut for one change

**Parameters:** `self`, `change` (one `(name, value)` pair).

**Return value:** a new instance.

```python
def process_single_change(self, change):
    # structure validation (name, value)
    name, value = change

    if name in self._constant_names_set:
        return with_constant(self, name, value)

    if name in self.meta.node_names_set:
        return with_composite(self, name, value)

    raise_with_any_unknown_name(self, name, value)
```

**The smallest routing unit in the entire subsystem** — just two
conditions, no grouping, no root-path detection. It exists purely so
that `with_any` does not need to run the full heavy machinery
`split_changes`/`get_top_composite_paths` for a single change — a direct
delegation to `with_constant` or `with_composite`, depending on where
`name` belongs.

[▲ Back to top](#-contents)

---

## `split_changes` — constants vs composites

**Parameters:** `self`, `changes` (tuple of pairs).

**Return value:** `tuple[ChangesTuple, ChangesTuple]` — `(constants,
composite)`.

```python
def split_changes(self, changes):
    constants, composite = [], []
    for inner_tuple in changes:
        # structure validation (name, value)
        name = inner_tuple[0]

        if name in self._constant_names_set:
            constants.append(inner_tuple)
        elif name in self.meta.node_names_set:
            composite.append(inner_tuple)
        else:
            raise_split_changes_unknown_name(self, name)

    return tuple(constants), tuple(composite)
```

**The first, most basic classification step of the entire `with_any`
pipeline** — it simply decides which of the two groups each change
belongs to. The two sets (`self._constant_names_set` and
`self.meta.node_names_set`, both inherited from
`NodesTuple` are the **canonical source of
truth** for this decision — no heuristics, no guessing based on value
type. Any name that matches neither set is immediately invalid
(`raise_split_changes_unknown_name`) — fail-fast, before the pipeline
tries to work with it.

[▲ Back to top](#-contents)

---

## `get_top_composite_paths` — root vs nested composites

**Parameters:** `composite` (tuple of `(name, value)` pairs, only
composites), `nodes_path_dict`.

**Return value:** `tuple[PathDict, PathDict]` — `(top_composite,
child_composite)`.

```python
def get_top_composite_paths(composite, nodes_path_dict):
    top_composite, top_composite_paths, child_composite = {}, [], {}

    sorted_paths = sorted(
        ((name, nodes_path_dict[name]) for name, _ in composite),
        key=lambda item: len(item[1]),
    )

    for key, path in sorted_paths:
        if not any(path[:len(parent)] == parent for parent in top_composite_paths):
            top_composite[key] = path
            top_composite_paths.append(path)
        else:
            child_composite[key] = path

    return top_composite, child_composite
```

**Sorting by path length (`len(item[1])`), not lexicographically.**  
This is different from `find_longest_keys`
(which sorts by path content) — here the goal is to find the **shortest**
(highest-level) paths first, because the traversal is **top-down**. Once
a path is recognized as “root” (`top_composite`), it is added to
`top_composite_paths`, and **all subsequent** paths that fall under it
(prefix test `path[:len(parent)] == parent`) automatically become
`child_composite` — regardless of depth. Short paths must be processed
**first**, so they can serve as a “filter” for deeper paths.

**The resulting `top_composite` is exactly the set applied in step 9 of
`with_any`.**  
And because `child_composite` paths are never applied again (only
verified), this step guarantees that no composite change is applied
**twice** or **in the wrong order** (a child before its parent would be
overwritten by the parent).

[▲ Back to top](#-contents)

---

## `split_constants_paths` — contained vs unique constants

**Parameters:** `constants` (tuple of `(name, value)` pairs),
`used_paths_dict` (paths of already applied root composites),
`nodes_path_dict`.

**Return value:** `tuple[PathDict, PathDict]` — `(contained, unique)`.

```python
def split_constants_paths(constants, used_paths_dict, nodes_path_dict):
    constants_paths = {name: nodes_path_dict[name] for name, _ in constants}

    root_prefixes = [
        path[:-1] if path and path[-1] == "_value" else path
        for path in used_paths_dict.values()
    ]

    contained, unique = {}, {}
    for key, path in constants_paths.items():
        if any(path[:len(prefix)] == prefix for prefix in root_prefixes):
            contained[key] = path
        else:
            unique[key] = path

    return contained, unique
```

**Normalizing `root_prefixes` (removing the trailing `"_value"`) is a
crucial detail that differs from the older version.**  
Composite node paths typically end with `_value` (their own value slot),
but the paths of their **inner elements** do not — they are separate
subpaths in the tree. Without removing `_value`, the prefix test
(`path[:len(prefix)] == prefix`) would never match a constant’s path
against a composite path ending in `_value`. Removing `_value` ensures
that `root_prefixes` represent the **structural branch** of the tree,
not the specific value node at its end. This fix is exactly what makes
the prefix test reliable for arbitrary nesting depth.

**Same “prefix” principle as in `get_top_composite_paths`, but reversed.**  
Instead of finding “who is the root” among composite paths, this function
checks “does this constant fall under an already-applied composite or
not”. `contained` (it does) is only **verified** in step 12 of
`with_any`; `unique` (it does not) is actually **applied** via
`with_constants`.

[▲ Back to top](#-contents)

---

## Why this entire orchestration is necessary

The whole purpose of `with_any` (and its four helper functions) can be
summarized in one sentence:  
**to prevent the same logical change from being applied twice, or in the
wrong order**, when the user provides a mix of changes at different
levels of the tree. Without this orchestration, it would be easy to
accidentally:

* apply a composite change, and then **again** (inconsistently) overwrite
  one of its inner elements with a direct value,
* apply a nested composite **before** its parent composite, which the
  parent would overwrite anyway,
* repeatedly recompute shared parents unnecessarily (handled by
  `find_longest_keys` inside `with_constants`, which `with_any` delegates to).

The result is that `with_any(self, many_different_changes)` always
produces **the same deterministic output**, regardless of the order in
which the user wrote the changes in the tuple — because the actual
application order (top-down, composites before constant verification) is
controlled by internal classification, not by input order.

[▲ Back to top](#-contents)

---
