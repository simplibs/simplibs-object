from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.instance import SimpleInstanceLike
    from ......_core.protocols.alias_typings import SnapshotDict


def reacalculate_owner_value(
    snapshot_dict: "SnapshotDict",
    owner: "SimpleInstanceLike",
) -> None:
    """
    Recalculates the composite value of the owner instance based on the
    current values of its direct inner nodes.
    """

    # 1. Load direct inner names
    owner_inners_name = (inner.meta.name_snake for inner in owner.meta.inners)

    # 2. Build a dictionary of inner values
    owner_inners_value_dict = {
        name: snapshot_dict[name]
        for name in owner_inners_name
    }

    # 3. Compute new composite value
    new_value = owner.logic(*owner_inners_value_dict)

    # 4. Write updated composite value into snapshot
    snapshot_dict[owner.meta.name_snake] = new_value


_DESIGN_NOTES = """
# reacalculate_owner_value

## Purpose
Recalculates the value of a composite node (“owner”) based on the current
values of its direct inner nodes. This function is a core part of the
immutability pipeline and ensures that composite values remain consistent
after any atomic or structural update.

## Architectural role
This function is used by:

- `with_constant`
- `with_constants`
- `with_composite`
- `with_any`
- snapshot-based reconstruction
- serialization and diffing utilities

It ensures that composite nodes always reflect the correct computed value
derived from their inner nodes.

## How it works
The function performs four deterministic steps:

1. **Collect inner node names**  
   Uses `owner.meta.inners` to determine which nodes contribute to the
   composite value.

2. **Load inner values from snapshot**  
   Reads values from `snapshot_dict`, which represents the current state of
   the object.

3. **Compute composite value**  
   Calls `owner.logic(...)`, the user-defined computation function associated
   with the composite node.

4. **Write updated value back into snapshot**  
   Ensures the snapshot reflects the recalculated composite value.

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
- `owner.logic` is pure and side-effect-free.

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
"""