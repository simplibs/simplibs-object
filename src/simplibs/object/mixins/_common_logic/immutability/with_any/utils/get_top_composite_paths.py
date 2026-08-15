from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.alias_typings import NodesPathDict, ChangesTuple, PathDict


def get_top_composite_paths(
    composite: "ChangesTuple",
    nodes_path_dict: "NodesPathDict",
) -> tuple["PathDict", "PathDict"]:
    """
    Returns only the composite paths closest to the root — i.e., those that
    are not subpaths of any other composite path in the dictionary.

    Logic:
    - Sort paths by length (shorter = higher in hierarchy)
    - For each path, check whether it is a prefix of any already stored root path
    - If not a prefix → it is a new root composite
    """

    # 1. Prepare variables
    top_composite = {}
    top_composite_paths = []
    child_composite = {}

    # 2. Build sorted list of (name, path) pairs
    composite_names = (name for name, _ in composite)
    sorted_paths = sorted(
        ((name, nodes_path_dict[name]) for name in composite_names),
        key=lambda item: len(item[1]),
    )

    # 3. Filter root composite paths
    for key, path in sorted_paths:

        # 3.1 Process top-level composites
        if not any(
            path[:len(parent)] == parent
            for parent in top_composite_paths
        ):
            top_composite[key] = path
            top_composite_paths.append(path)

        # 3.2 Process inner composites
        else:
            child_composite[key] = path

    # 4. Return both dictionaries
    return top_composite, child_composite


_DESIGN_NOTES = """
# get_top_composite_paths

## Purpose
Identifies which composite nodes in a change set are **root composites** and
which are **child composites**.  
Root composites are those whose structural paths are not prefixes of any other
composite path.  
Child composites are those that lie inside another composite’s structural path.

This function is essential for determining the correct update order in the
[with_any](ca://s?q=Explain_with_any) pipeline.

## Architectural role
This function is used by:

- [with_any](ca://s?q=Explain_with_any) — mixed update pipeline  
- indirectly by composite recalculation logic  
- debugging and structural validation tools  

It provides the structural classification needed to apply composite updates
in the correct hierarchical order.

## How it works
The function performs four deterministic phases:

### 1. Prepare containers
Creates dictionaries for:
- **top_composite** — root-level composites  
- **child_composite** — nested composites  
And a list `top_composite_paths` for prefix comparison.

### 2. Sort composite paths by length
Shorter paths represent higher-level composites.  
Sorting ensures that parent paths are processed before child paths.

### 3. Classify composites
For each `(name, path)` pair:

- If the path is **not** a prefix of any already stored root path →  
  it is a **root composite**.

- If the path **is** a prefix match →  
  it is a **child composite**.

This classification is purely structural and deterministic.

### 4. Return both dictionaries
The caller receives:
- root composites → to be applied first  
- child composites → validated after root updates  

## Why root composites matter
Composite updates must be applied **from the top down**:

- Root composites define the highest-level structural changes  
- Child composites must be validated **after** root updates  
- This prevents inconsistent or impossible composite states  

Correct ordering ensures:

- deterministic immutability behavior  
- minimal recomputation  
- structural correctness  

## Deterministic behavior
The classification is deterministic because:

- sorting is stable  
- prefix comparison is structural  
- metadata paths are canonical  
- output ordering matches structural hierarchy  

This determinism is essential for immutability pipelines.

## Stability guarantee
Any change to this function would affect:

- composite update order  
- immutability correctness  
- validation logic in `with_any`  
- debugging behavior  

Therefore, `get_top_composite_paths` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to path metadata (`nodes_path_dict`).  
"""