from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.alias_typings import NodesPathDict, PathDict, ChangesTuple


def split_constants_paths(
    constants: "ChangesTuple",
    used_paths_dict: "PathDict",
    nodes_path_dict: "NodesPathDict",
) -> tuple["PathDict", "PathDict"]:
    """
    Splits constant paths into two groups:

    - contained: paths that lie inside one of the provided root paths
    - unique:    paths that do not fall under any root path
    """

    # 1. Build dictionary of constant paths
    constants_paths = {name: nodes_path_dict[name] for name, _ in constants}
    used_paths = used_paths_dict.values()

    # 2. Prepare containers
    contained = {}
    unique = {}

    # 3. Classify paths
    for key, path in constants_paths.items():

        # 3.1 Path starts with any root → contained
        if any(
            path[:len(used_path)] == used_path
            for used_path in used_paths
        ):
            contained[key] = path

        # 3.2 Otherwise → unique
        else:
            unique[key] = path

    # 4. Return both dictionaries
    return contained, unique


_DESIGN_NOTES = """
# split_constants_paths

## Purpose
Splits constant paths into **contained** and **unique** groups based on their
relationship to a set of root composite paths.  
This function is used to determine which constant updates belong inside already
updated composite branches and which constants must be applied separately.

It is a structural helper for the [with_any](ca://s?q=Explain_with_any) pipeline.

## Architectural role
This function is used by:

- [with_any](ca://s?q=Explain_with_any) — mixed update pipeline  
- indirectly by composite recalculation logic  
- debugging and structural validation tools  

It provides the classification needed to correctly apply constant updates
after composite updates.

## How it works
The function performs four deterministic phases:

### 1. Build constant path dictionary
Each constant `(name, value)` pair is mapped to its structural path using
`nodes_path_dict`.

### 2. Prepare containers
Creates two dictionaries:
- **contained** — constants lying inside root composite paths  
- **unique** — constants outside all root composite paths  

### 3. Classify paths
For each constant path:

- If the path **starts with** any root path →  
  it is **contained**.

- Otherwise →  
  it is **unique**.

Prefix comparison is structural and deterministic.

### 4. Return both dictionaries
The caller receives:
- contained constants → validated against composite updates  
- unique constants → applied after composite updates  

## Why this classification matters
Composite updates may already modify some inner constants.  
To avoid double updates or inconsistent states:

- contained constants must be **validated**, not applied  
- unique constants must be **applied** after composite updates  

This ensures:

- correct dependency ordering  
- minimal recomputation  
- structural consistency  
- deterministic immutability behavior  

## Deterministic behavior
The classification is deterministic because:

- path comparison uses canonical structural paths  
- metadata ordering is stable  
- prefix matching is pure and side-effect-free  
- output ordering matches input ordering  

This determinism is essential for immutability pipelines.

## Integration requirements
The function assumes the instance implements:

- [NodesDicts](ca://s?q=Explain_NodesDicts_mixin) — provides path metadata  
- [Snapshot](ca://s?q=Explain_Snapshot_mixin) — indirectly used by downstream functions  

Without these mixins, the pipeline cannot classify updates correctly.

## Stability guarantee
Any change to this function would affect:

- constant update order in `with_any`  
- composite validation logic  
- immutability correctness  
- debugging behavior  

Therefore, `split_constants_paths` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side-effect-free.  
- It is not part of the public API; it is used internally by mixins.  
- All structural logic is delegated to path metadata (`nodes_path_dict`).  

"""