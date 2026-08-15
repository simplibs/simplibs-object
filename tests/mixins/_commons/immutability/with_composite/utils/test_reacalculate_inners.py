from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.metadata import SimpleMetadataLike
    from ......_core.protocols.alias_typings import SnapshotDict


def reacalculate_inners(
    snapshot_dict: "SnapshotDict",
    meta: "SimpleMetadataLike",
    new_value: Any,
) -> None:
    """
    Recalculates the values of inner nodes for a composite based on the
    provided new composite value.
    """

    # 1. Load inner metadata objects
    inners_meta = (inner.meta for inner in meta.inners)

    # 2. Compute decomposed inner values
    inners_value = meta.decompose(new_value)

    # 3. Iterate through metadata and computed values
    for inner_meta, inner_value in zip(inners_meta, inners_value):

        # 3.1 Write the inner value
        snapshot_dict[inner_meta.name_snake] = inner_value

        # 3.2 If the inner node is itself a composite → recurse
        if not inner_meta.is_constant:
            reacalculate_inners(snapshot_dict, inner_meta, inner_value)


_DESIGN_NOTES = """
# reacalculate_inners

## Purpose
Recalculates the values of all inner nodes belonging to a composite node.
This function ensures that when a composite value changes, all of its
decomposed inner values are updated accordingly — including nested composites.

It is the structural counterpart to [reacalculate_owner_value](ca://s?q=Explain_recalculate_owner_value).

## Architectural role
This function is used by:

- [with_composite](ca://s?q=Explain_with_composite) — composite-level updates  
- [with_any](ca://s?q=Explain_with_any) — mixed updates  
- snapshot reconstruction  
- immutability pipelines  
- debugging and diffing tools  

It ensures that composite nodes remain structurally consistent after updates.

## How it works
The function performs three deterministic steps:

### 1. Load inner metadata
Retrieves metadata objects for all direct inner nodes of the composite.

### 2. Decompose composite value
Uses `meta.decompose(new_value)` to compute the values of all inner nodes.
This decomposition is user-defined and reflects the composite’s logic.

### 3. Write values and recurse
For each inner node:

- its value is written into the snapshot dictionary,  
- if the inner node is itself composite, the function calls itself recursively.

This guarantees that nested composite structures are fully updated.

## Why recursion is required
Composite nodes may contain other composite nodes.  
Updating only the first level would leave deeper levels inconsistent.

Recursion ensures:

- full structural propagation,  
- correct nested decomposition,  
- deterministic immutability behavior,  
- minimal recomputation (only affected branches are updated).

## Deterministic behavior
The update is deterministic because:

- decomposition order is stable,  
- metadata ordering is canonical,  
- recursion follows structural hierarchy,  
- snapshot dictionary uses canonical `name_snake` keys.

This determinism is essential for immutability pipelines.

## Stability guarantee
Any change to this function would affect:

- composite recalculation,  
- immutability correctness,  
- snapshot consistency,  
- debugging tools,  
- serialization behavior.

Therefore, `reacalculate_inners` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to metadata (`meta.inners`, `meta.decompose`).  

"""