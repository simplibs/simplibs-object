from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
from ._get_collision_path import _get_collision_path
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_if_collision_with_owner_class(
    collision_name: str,
    owner_snake_name: str,
    inner_culprit: "SimpleClassLike",
    owner_class: "SimpleClassLike",
) -> None:
    """Validates collision between inner name and owner class name."""

    # 1. Check collision
    if collision_name != owner_snake_name:
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Compute culprit path
    culprit_path = _get_collision_path(inner_culprit, collision_name) or inner_culprit.__name__
    full_path = f"{class_name} -> {culprit_path}"
    leaf_name = culprit_path.split("/")[-1]

    # 4. Raise error
    raise SimpleDefinitionError(
        error_name=error_name,
        label="owner_class_name_collision",
        expected="Unique name_snake across entire composition tree",
        value=collision_name,
        problem="Nested component uses the same identifier as its root owner class.",
        context=context,
        how_to_fix=(
            f"Conflicting identifier: '{collision_name}'.",
            f"Path to offending component: {full_path}.",
            f"Rename class '{leaf_name}' or rename root class '{class_name}'.",
            "Every class in the composition hierarchy must have a unique name_snake.",
        ) + acceptable,
        exception=NameError,
    )



_DESIGN_NOTES = """
# validate_if_collision_with_owner_class

## Purpose
Detects the most severe naming conflict: an inner element sharing the same
`name_snake` as the owner class. This would break the entire composition tree.

## Behavior
1. Compares `collision_name` with the owner’s `name_snake`.
2. If equal, computes a structural path to the culprit using `_get_collision_path`.
3. Raises a structured `SimpleDefinitionError` with precise remediation steps.

## Notes
This validator is separate from sibling-collision checks because collisions with
the owner class have different semantics and require different remediation.
"""