from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_inners import _exception_info_for_inners
# Inners
from ._get_collision_path import _get_collision_path
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_if_collision_with_owner_class(
    collision_name: str,
    owner_snake_name: str,
    inner_culprit: "SimpleClassLike",
    owner_class: "SimpleClassLike"
) -> None:
    """Validates whether a detected conflicting name matches the root owner class identifier and raises a specific error."""

    # 1. Exception condition
    if collision_name == owner_snake_name:

        # 2. Variable resolution
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_inners(owner_class)

        # Resolve the internal path to the component causing the collision
        culprit_path = _get_collision_path(inner_culprit, collision_name) or inner_culprit.__name__
        full_path = f"{class_name} -> {culprit_path}"
        target_leaf_name = culprit_path.split("/")[-1]

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Name collision with root owner class",
            expected="Globally unique identifier names (name_snake) across the entire composition tree hierarchy.",
            problem="An internal nested component shares the exact same identifier name as its root owner class.",
            context=context,
            how_to_fix=(
                f"Conflicting name identifier: '{collision_name}'.",
                f"Path to the offending component: {full_path}.",
                f"Rename the class '{target_leaf_name}' within the nested composition subtree.",
                f"Or rename the root owner class '{class_name}' itself.",
                "Every single class registered within the composition hierarchy must resolve to a unique 'name_snake' value.",
            ),
            exception=NameError
        )


_DESIGN_NOTES = """
# validate_if_collision_with_owner_class

## Purpose
This validation handles the most severe structural naming conflict: the recursive loop paradox. 
It guards against scenarios where a nested component (or any of its downstream children) attempts 
to use an identifier name identical to the root class containing it.

## Control Flow Strategy
Designed as a passive early-exit guardian. If the `collision_name` does not match the 
`owner_snake_name`, the function instantly returns without performing any extra operational overhead. 
This allows the compiler pipeline to maintain a clean, linear execution pattern without complex 
nested conditional branches.

## Architectural Separation
Conflicts with the root owner possess an entirely different structural semantic than sibling 
collisions. Separating this check into a dedicated module allows us to deliver pinpoint accurate 
remediation messages tailored to the hierarchical parent-child relationship, vastly optimizing 
the debugging experience.
"""