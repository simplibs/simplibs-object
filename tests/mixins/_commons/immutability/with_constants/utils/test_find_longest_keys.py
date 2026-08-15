from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.alias_typings import PathDict, NamesTuple


def find_longest_keys(
    path_dict: "PathDict",
) -> "NamesTuple":
    """
    Finds the keys whose paths represent terminal (deepest) nodes within
    the provided path dictionary.
    """

    # 1. Convert dictionary into a list of (key, path) pairs
    #    and sort them by their path (index 1)
    sorted_path = sorted(path_dict.items(), key=lambda x: x[1])
    longest_keys = []

    # 2. Iterate and compare paths
    for i in range(len(sorted_path) - 1):
        key, path = sorted_path[i]
        _, next_path = sorted_path[i + 1]

        # If the next path starts with the current path,
        # the current one is an intermediate node → skip it.
        if next_path[:len(path)] == path:
            continue

        # Otherwise, this is a terminal node → store its key.
        longest_keys.append(key)

    # The last element in the sorted list is always terminal
    longest_keys.append(sorted_path[-1][0])

    return tuple(longest_keys)


_DESIGN_NOTES = """
# find_longest_keys

## Purpose
Identifies the “deepest” or terminal nodes among a set of changed paths.
This function is used in the immutability pipeline to determine which composite
owners must be recalculated after constant updates.

It ensures that recalculation starts from the deepest affected nodes and moves
upward, preserving structural correctness.

## Architectural role
This function is used by:

- [with_constants](ca://s?q=Explain_with_constants) — batch constant updates  
- [with_any](ca://s?q=Explain_with_any) — mixed updates  
- [with_composite](ca://s?q=Explain_with_composite) — composite updates  

It determines the minimal set of composite nodes that must be recalculated.

## How it works
The function performs three deterministic steps:

1. **Sort paths by structural depth**  
   Sorting ensures that shorter (parent) paths appear before longer (child)
   paths.

2. **Compare each path with the next one**  
   If the next path starts with the current path, the current path is a parent
   and not a terminal node.

3. **Collect terminal nodes**  
   Terminal nodes are those whose paths are not prefixes of any subsequent path.

The last element in the sorted list is always terminal.

## Why terminal nodes matter
Recalculating composite nodes must begin at the deepest affected point in the
structure. Starting from parents would produce incorrect values because their
children may not yet be updated.

Terminal nodes guarantee:

- correct recalculation order,
- minimal recomputation,
- structural consistency,
- deterministic behavior.

## Deterministic behavior
The output is deterministic because:

- sorting is stable,
- path comparison is structural,
- terminal detection is positional,
- output order matches structural depth.

This determinism is essential for immutability pipelines.

## Stability guarantee
Any change to this function would affect:

- composite recalculation order,
- immutability correctness,
- snapshot consistency,
- debugging tools.

Therefore, `find_longest_keys` is treated as a **core invariant** of the
immutability subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to path ordering.
"""