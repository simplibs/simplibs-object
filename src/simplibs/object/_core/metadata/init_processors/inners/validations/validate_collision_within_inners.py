from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
from ._get_collision_path import _get_collision_path
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_collision_within_inners(
    collision_name: str,
    owner_snake_name: str,
    raw_inners: tuple["SimpleClassLike", ...],
    current_inner: "SimpleClassLike",
    owner_class: "SimpleClassLike",
) -> None:
    """Validates sibling name collisions inside _inners."""

    # 1. Check collision (ignore owner-class collisions)
    if not collision_name or collision_name == owner_snake_name:
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Find first culprit (the one that registered the name earlier)
    first_path = None
    for previous_inner in raw_inners:
        if collision_name in previous_inner.meta.node_names_set:
            first_path = _get_collision_path(previous_inner, collision_name)
            break

    first_full = f"{class_name} -> {first_path}"

    # 4. Find second culprit (the current conflicting component)
    second_path = _get_collision_path(current_inner, collision_name)
    second_full = f"{class_name} -> {second_path}"

    # 5. Raise error
    raise SimpleDefinitionError(
        error_name=error_name,
        label="inner_name_collision",
        expected="Unique name_snake across all inner components",
        value=collision_name,
        problem="Two inner components share the same identifier.",
        context=context,
        how_to_fix=(
            f"Conflicting identifier: '{collision_name}'.",
            f"Existing definition: {first_full}.",
            f"Duplicate declaration: {second_full}.",
            f"Rename one of the conflicting components inside '{class_name}'.",
            "Ensure you did not accidentally register the same class twice.",
            "name_snake must be globally unique within the composition tree.",
        ) + acceptable,
        exception=NameError,
    )


_DESIGN_NOTES = """
# validate_collision_within_inners

## Purpose
Detects naming collisions between sibling inner components.  
This validator is triggered only after owner-class collisions have been ruled out.

## Behavior
1. Checks whether the collision is a sibling-level conflict.
2. Locates the first component that registered the name.
3. Locates the second component causing the duplicate.
4. Builds breadcrumb paths using `_get_collision_path`.
5. Raises a structured `SimpleDefinitionError`.

## Notes
This validator is a strict enforcement barrier.  
If reached, a naming conflict is guaranteed and compilation must stop.
"""