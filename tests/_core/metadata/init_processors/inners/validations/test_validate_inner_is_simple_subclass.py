from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_inner_is_simple_subclass(
    inner: "SimpleClassLike",
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that an inner element inherits from SimpleConstant."""

    # Lazy import to avoid circular dependencies
    from .......SimpleConstant import SimpleConstant

    # 1. Check subclass relationship
    inner: type
    if issubclass(inner, SimpleConstant):
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Raise error
    raise SimpleMetadataError(
        error_name=error_name,
        label="inner_not_simple_subclass",
        expected="Subclass of SimpleConstant or SimpleObject",
        value=inner,
        problem=f"Inner element '{inner}' does not inherit from SimpleConstant.",
        context=context,
        how_to_fix=(
            "Ensure the class inherits from SimpleConstant or SimpleObject.",
            "Verify the inheritance tree of the failing class.",
            "Check that you imported the correct class definition.",
        ) + acceptable,
        exception=TypeError,
    )



_DESIGN_NOTES = """
# validate_inner_is_simple_subclass

## Purpose
Ensures that each inner element inherits from the framework’s base classes
(SimpleConstant or SimpleObject).

## Behavior
1. Checks `issubclass(inner, SimpleConstant)`.
2. If invalid, retrieves shared diagnostic info.
3. Raises a structured `SimpleMetadataError`.

## Notes
This validator assumes the inner element has already passed `validate_inner_is_class`.
It focuses exclusively on inheritance correctness.
"""