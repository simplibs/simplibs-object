from typing import TYPE_CHECKING
# Inners
from ._collect_nodes_data import _collect_nodes_data
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.core_mixins import NodesTupleProtocol
    from ....._core.protocols.alias_typings import NodesTuple


def build_nodes_tuple(
    self: "NodesTupleProtocol",
) -> "NodesTuple":
    """
    Builds a tuple of (instance, path) pairs representing the full structural
    tree of the object. The path contains snake_case names describing how to
    reach each node from the root.
    """

    # 1. Prepare accumulator
    nodes_list = []

    # 2. Recursively collect all nodes
    _collect_nodes_data(
        instance=self,
        path=(),
        nodes_list=nodes_list,
    )

    # 3. Convert to tuple and return
    return tuple(nodes_list)


_DESIGN_NOTES = """
# build_nodes_tuple

## Purpose
Creates the canonical `nodes_tuple` structure used throughout the Simple system.
This structure is a flat, ordered tuple of `(instance, path)` pairs representing
every node in the object tree. It serves as the **primary source of truth** for
mixins that need to inspect or manipulate the internal structure of an object.

## Architectural role
`build_nodes_tuple` is the public-facing wrapper around `_collect_nodes_data`.
Its responsibilities are intentionally minimal:

1. Prepare an accumulator list.
2. Delegate recursive traversal to `_collect_nodes_data`.
3. Freeze the result into an immutable tuple.

This separation keeps traversal logic isolated while providing a clean,
deterministic API for mixins.

## Why this function exists
Many mixins rely on a consistent structural representation:

- `NodesTupleMixin`  
  Builds `_nodes_tuple`, `_node_names_tuple`, `_constant_names_tuple`.

- Snapshot mixins  
  Use `nodes_tuple` to create and restore snapshots.

- Immutability helpers  
  Use it to compute new instances, propagate changes, and recalculate composites.

- History mixin  
  Uses it to track structural changes over time.

- Serialization mixins  
  Convert `nodes_tuple` into JSON or dict representations.

By centralizing the creation of this structure, the system ensures:

- deterministic traversal order,
- consistent path construction,
- stable behavior across all mixins.

## Deterministic output
The resulting tuple is:

- **ordered** — depth-first traversal,
- **complete** — includes constants and composites,
- **stable** — identical for identical object structures,
- **immutable** — safe for caching and snapshotting.

This determinism is essential for immutability pipelines and diffing logic.

## Stability guarantee
Any change to this function would affect:

- snapshot creation,
- immutability behavior,
- composite recalculation,
- history tracking,
- serialization,
- and all mixins relying on `nodes_tuple`.

Therefore, the function is treated as a **core invariant** of the Simple system.

## Notes
- This function is intentionally simple and side-effect-free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to `_collect_nodes_data`.

"""