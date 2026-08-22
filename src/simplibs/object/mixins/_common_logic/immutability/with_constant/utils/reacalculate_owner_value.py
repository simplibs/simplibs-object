from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.instance import SimpleInstanceLike
    from ......_core.protocols.alias_typings import SnapshotDict


def reacalculate_owner_value(
    snapshot_dict: "SnapshotDict",
    owner: "SimpleInstanceLike",
) -> None:
    """
    Recalculates composite values along the owner hierarchy up to the root,
    based on the current values of their direct inner nodes.
    """

    # 1. Initialize cursor at the starting owner
    current_owner = owner

    # 2. Traverse upwards through the owner chain until reaching root (UNSET)
    while current_owner is not UNSET:

        # 2.1 Load direct inner names
        owner_inners_name = (inner.meta.name_snake for inner in current_owner.meta.inners)

        # 2.2 Build a dictionary of inner values
        owner_inners_value_dict = {
            name: snapshot_dict[name]
            for name in owner_inners_name
        }

        # 2.3 Compute new composite value via owner metadata logic
        new_value = current_owner.meta.logic(**owner_inners_value_dict)

        # 2.4 Write updated composite value into snapshot
        snapshot_dict[current_owner.meta.name_snake] = new_value

        # 2.5 Move to the next parent composite owner
        current_owner = current_owner.owner


_DESIGN_NOTES = """
# reacalculate_owner_value

## Purpose
Recalculates the value of composite nodes (“owners”) up the hierarchy based on the
current values of their direct inner nodes. This function is a core part of the
immutability pipeline and ensures that composite values remain consistent
after any atomic or structural update across all nesting depths.

## Architectural role
This function is used by:

- `with_constant`
- `with_constants`
- `with_composite`
- `with_any`
- snapshot-based reconstruction
- serialization and diffing utilities

It ensures that composite nodes at every level reflect the correct computed value
derived from their inner nodes.

## How it works
The function iteratively walks up the owner hierarchy (`owner.owner`):

1. **Initialize owner cursor**  
   Starts with the direct owner node provided in arguments.

2. **Collect inner node names**  
   Uses `current_owner.meta.inners` to determine which nodes contribute to the
   composite value.

3. **Load inner values from snapshot**  
   Reads values from `snapshot_dict`, which represents the intermediate state
   of the object.

4. **Compute composite value directly via metadata logic**  
   Calls `current_owner.meta.logic(**owner_inners_value_dict)` directly. This bypasses
   argument preprocessing and validation overhead since values in snapshot
   are already validated.

5. **Write updated value back into snapshot**  
   Ensures the snapshot reflects the recalculated composite value under
   `current_owner.meta.name_snake`.

6. **Propagate upwards**  
   Advances `current_owner = current_owner.owner` until the root is reached (`UNSET`).

## Why snapshot_dict is used
Composite recalculation happens *before* a new instance is created.  
Using `snapshot_dict` allows:

- atomic updates,
- batch updates,
- multi-step recalculation,
- consistent immutability behavior,
- safe merging of changes.

The snapshot acts as a temporary workspace for recalculation.

## Deterministic behavior
Composite recalculation is deterministic because:

- inner nodes are processed in a stable order,
- `name_snake` identifiers are canonical,
- snapshot values are flat and predictable,
- `owner.meta.logic` is pure and side-effect-free,
- hierarchy traversal follows unambiguous structural parent links (`_owner`).

This determinism is essential for immutability pipelines.

## Stability guarantee
Any change to this function would affect:

- composite recalculation,
- immutability behavior,
- serialization consistency,
- snapshot reconstruction,
- debugging tools.

Therefore, `reacalculate_owner_value` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to `owner.meta.inners`.
- All execution logic delegates directly to `owner.meta.logic`.
"""