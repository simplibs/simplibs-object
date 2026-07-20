from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def _get_collision_path(
    current_class: "SimpleClassLike",
    collision_name: str,
) -> str | None:
    """Recursively traces the structural path to the class causing a name collision.

    Returns a string path in the format 'ClassA/ClassB/ClassC', where ClassC is
    the actual definition owner of the conflicting 'collision_name'.
    """

    # 1. Evaluate if the collision originates directly within this class level
    if current_class.meta.name_snake == collision_name:
        return current_class.__name__

    # 2. If this node is not the direct culprit, scan its downstream components (_inners)
    raw_inners = getattr(current_class, "_inners", ())

    for inner in raw_inners:
        # Utilize node_names_set as a fast pre-filter index before initiating recursion
        if collision_name in inner.meta.node_names_set:
            # Perform deep recursive traversal down the component branch
            sub_path = _get_collision_path(inner, collision_name)

            if sub_path:
                # Construct the tracking breadcrumb trail: Current -> Target
                return f"{current_class.__name__}/{sub_path}"

    return None


_DESIGN_NOTES = """
# _get_collision_path

## Purpose
Acts as a high-precision tree traversal utility designed to map structural paths to conflicting 
components. Instead of just throwing a vague collision error, this utility generates a transparent 
breadcrumb trail (e.g., `Order/Delivery/Address`), providing excellent Developer Experience (DX).

## Efficiency & Indexing Strategy
Traversing deep nested tree structures recursively can easily become an performance bottleneck. 
To bypass expensive lookups, this helper utilizes an indexing optimization strategy:
1. Every component maintains a pre-calculated `meta.node_names_set` containing all names present 
   in its sub-tree.
2. The loop evaluates `collision_name in inner.meta.node_names_set` as an O(1) membership filter.
3. The expensive recursive deep dive is *only* initiated on the exact structural branch that is 
   guaranteed to contain the culprit class.

## Interface & Boundaries
This function is deliberately marked as internal with a leading underscore (`_`) and isolated into 
a `utils` submodule. It does not perform validation checks or raise exceptions; its single 
responsibility is deterministic path computation, returning either a formatted string path 
or `None` if no match is found.
"""