# 🔒 `with_composite` — Immutable Update of a Composite Node

The structural counterpart to [`with_constant`](README_WITH_CONSTANT.md) —
handles situations where the value of a **composite** node changes (rather
than a leaf constant). Unlike a constant, it must handle recalculation in
**both directions**: downward into inner elements (decomposition) and
upward toward parent composites.

> The same integration requirement as for `with_constant`: the instance must
> inherit from `Snapshot` and `NodesDicts`.

```text
with_composite
├── with_constant             (delegation if name actually refers to a constant)
├── create_snapshot_dict      (shared with with_constant)
├── reacalculate_inners       (new: propagation DOWNWARD)
├── reacalculate_owner_value  (shared with with_constant: propagation UPWARD)
└── create_new_instance       (shared with with_constant)
```

---

## 🧭 Contents

* [`with_composite` — main pipeline](#with_composite--main-pipeline)
* [`reacalculate_inners` — downward recalculation](#reacalculate_inners--downward-recalculation)

[⬅️ Back to Immutable methods](../README_IMMUTABLE_METHODS.md#with_composite)

---

## `with_composite` — main pipeline

**Parameters:** `self`, `name` (name of the composite node), `new_value`.

**Return value:** a new instance.

**Nine steps:**

```python id="b7nq2k"
def with_composite(self, name, new_value):
    if name in self._constant_names_set:
        return with_constant(self, name, new_value)      # 1. delegation

    if name not in self.meta.node_names_set or not self.meta.is_decomposeable:
        validate_composite_name_exists(self, name)         # 2. existence + decomposability validation
        validate_composite_is_decomposeable(self, name)

    instance, path = self._nodes_dict[name]
    instance.validate(new_value)                            # 3. value validation

    snapshot_dict = create_snapshot_dict(self._nodes_tuple)  # 4.
    snapshot_dict[name] = new_value                          # 5.

    reacalculate_inners(snapshot_dict, instance.meta, new_value)   # 6. DOWNWARD
    reacalculate_owner_value(snapshot_dict, instance.owner)        # 7. UPWARD

    new_snapshot = tuple(snapshot_dict.values())              # 8.
    return create_new_instance(self, new_snapshot)             # 9.
```

**Step 1 — delegation to `with_constant` is a deliberate,
user-friendly shortcut.** `with_composite` itself does not know (and does
not need to know) in advance whether `name` refers to a constant or a
composite — it simply checks, and if it is a constant, skips the rest of
the logic and delegates to the specialized, simpler function. This allows
higher-level layers (`with_any`, see
[README_WITH_ANY](README_WITH_ANY.md)) to avoid having to handle this
distinction themselves wherever calling `with_composite` might be useful.

**Two independent recalculation phases — downward (step 6) and upward
(step 7) — in this exact order.** This is the key architectural difference
from `with_constant`, which only handles one direction (upward). A composite
node **has** inner elements that must remain consistent with its new value
(hence step 6, `reacalculate_inners`), while at the same time it may itself
be an inner element of something higher in the tree (hence step 7, using
the same `reacalculate_owner_value` as `with_constant`). The "downward,
then upward" order makes sense — `reacalculate_inners` only operates on the
subtree below `name` and does not depend on anything above it, while
`reacalculate_owner_value` reads values from `snapshot_dict` (including
those just written by step 6, if a parent directly depends on them), so it
must run only after the downward propagation is complete.

[▲ Back to top](#-contents)

---

## `reacalculate_inners` — downward recalculation

**Parameters:** `snapshot_dict` (mutated in place), `meta` (metadata of the
composite node whose value has just changed), `new_value`.

**Return value:** `None`.

```python id="v5m8rq"
def reacalculate_inners(snapshot_dict, meta, new_value):
    inners_meta = (inner.meta for inner in meta.inners)
    inners_value = meta.decompose(new_value)

    for inner_meta, inner_value in zip(inners_meta, inners_value):
        snapshot_dict[inner_meta.name_snake] = inner_value

        if not inner_meta.is_constant:
            reacalculate_inners(snapshot_dict, inner_meta, inner_value)
```

**Recursive, unlike `reacalculate_owner_value` (which is iterative).**
This difference has a structural reason: the path **upward** is always
linear (a node has at most one `_owner`, so a `while` loop is sufficient),
whereas the path **downward** **branches** (a composite node can have
multiple `_inners`, each of which can contain further nested `_inners`) —
so it naturally requires recursion rather than a simple loop.

**It uses `meta.decompose(new_value)` directly, following the same
"raw metadata call" pattern as `reacalculate_owner_value` uses
`meta.logic(...)`** (see
[README_WITH_CONSTANT](README_WITH_CONSTANT.md#reacalculate_owner_value--recalculation-toward-the-root)) —
it bypasses the public `decompose_value` (compare with
[README_SIMPLE_OBJECT](../../../../core/README_SIMPLE_OBJECT)), because
`new_value` has already passed validation at this point in the pipeline
(`instance.validate(new_value)` in `with_composite`), so a second validation
would be unnecessary.

**The `if not inner_meta.is_constant` condition is what makes the recursion
terminate even for arbitrarily deep trees.** If an inner element is an atom
(`is_constant`), recursion is not started for it — an atom has nothing
further to decompose. If it is another composite, the function is called
again with the same `snapshot_dict` (shared and mutated throughout the
entire recursion) and new `inner_meta`/`inner_value` — so the same mechanism
propagates to arbitrary depths of nested composites, exactly as
[`_recalculate_inners`](../../../../metadata/instance/README_COMPOSITE_CLASS.md)
does for mutable instances, except that here it operates on
`snapshot_dict` instead of directly on instance slots.

[▲ Back to top](#-contents)

➡️ Continued in: [README_WITH_ANY](README_WITH_ANY.md)
