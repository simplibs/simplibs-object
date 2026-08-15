from typing import TYPE_CHECKING
# Outers
from ...._commons.constants import VALUE
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.instance import SimpleInstanceLike
    from ....._core.protocols.alias_typings import PathTuple, NodeItem


def _collect_nodes_data(
    instance: "SimpleInstanceLike",
    path: "PathTuple",
    nodes_list: list["NodeItem"],
) -> None:
    """
    Recursively traverses the entire instance structure and appends
    (instance, path) pairs into `nodes_list`.

    Each pair represents a node in the object tree, where `path` is a tuple
    of snake_case names describing how to reach the node from the root.
    """

    # 1. Add current node (constant)
    if instance.meta.is_constant:
        nodes_list.append((instance, path))
        return

    # 2. Add current node (composite)
    else:
        nodes_list.append((instance, path + (VALUE,)))

    # 3. Process composite inners
    for inner in instance.meta.inners:

        # 3.1 Extract metadata
        inner_meta = inner.meta

        # 3.2 Load inner instance
        inner_instance = getattr(instance, inner_meta.name_private)

        # 3.3 Recursive descent
        _collect_nodes_data(
            instance=inner_instance,
            path=path + (inner_meta.name_snake,),
            nodes_list=nodes_list,
        )


_DESIGN_NOTES = """
# _collect_nodes_data

## Purpose
Internal recursive walker that builds the foundational `(instance, path)` pairs
used throughout the Simple system. It is the core mechanism behind
`NodesTupleMixin`, snapshot creation, immutability pipelines, history tracking,
and composite recalculation.

The function produces a **flat, ordered list** representing the entire object
tree, where each entry contains:

- the instance of a node,
- the path tuple describing how to reach it from the root.

This list is later converted into `nodes_tuple`, the canonical structure used by
many mixins.

## Architectural role
This function is one of the deepest internal utilities in the Simple system.
It provides:

### 1. Deterministic structural traversal
The order of nodes is stable and predictable:
- root first,
- then all constants,
- then all composites,
- depth‑first traversal.

### 2. Unified representation of object structure
Every mixin that needs to understand the object tree relies on the same
canonical representation:
- immutability helpers,
- snapshot creation,
- history mixin,
- serialization,
- composite recalculation,
- diffing and patching.

### 3. Path construction
Each node receives a `path` tuple containing snake_case names of attributes
leading to it. This path is used for:
- snapshot dictionaries,
- change propagation,
- composite recalculation,
- debugging and introspection.

### 4. Constant vs composite distinction
The function uses `instance.meta.is_constant` to determine:
- whether the node is terminal,
- whether to append `(VALUE,)` to the path,
- how composite recalculation should treat the node.

This distinction is essential for immutability pipelines.

## Why this function is recursive
The Simple system supports arbitrarily deep composite structures.  
A recursive walker ensures:
- clarity,
- correctness,
- minimal code,
- deterministic traversal order.

## Stability guarantee
This function is a **core invariant** of the Simple architecture.  
Any change to traversal order or path construction would break:

- snapshot creation,
- immutability pipelines,
- composite recalculation,
- history tracking,
- serialization,
- diffing,
- and several mixins relying on `nodes_tuple`.

Therefore, modifications must be carefully reviewed.

## Notes
- This function is intentionally low‑level and not part of the public API.
- It is used exclusively by `build_nodes_tuple`.
- It must remain fast, predictable, and side‑effect‑free.

"""