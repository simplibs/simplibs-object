from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_inner_is_not_simple_class(
    inner: "SimpleClassLike",
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that inner is not SimpleConstant or SimpleObject."""

    # Lazy imports to avoid circular dependencies
    from .......SimpleConstant import SimpleConstant
    from .......SimpleObject import SimpleObject

    # 1. Check identity
    if inner is not SimpleConstant and inner is not SimpleObject:
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Raise error
    raise SimpleDefinitionError(
        error_name=error_name,
        label="inner_is_base_class",
        expected="Concrete subclass of SimpleConstant or SimpleObject",
        value=inner,
        problem=f"Class '{class_name}' declares base class '{inner.__name__}' inside _inners.",
        context=context,
        how_to_fix=(
            "Use concrete subclasses, not the base framework classes.",
            "SimpleObject and SimpleConstant serve only as inheritance roots.",
            "Replace this reference with a specific subclass representing actual data.",
        ) + acceptable,
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_inner_is_not_simple_class

## Purpose
Ensures that `_inners` does not contain the raw base classes `SimpleObject`
or `SimpleConstant`. Only concrete subclasses are allowed.

## Behavior
1. Compares the inner element using identity (`is`) with the base classes.
2. If invalid, retrieves shared diagnostic info.
3. Raises a structured `SimpleDefinitionError`.

## Notes
This validator complements `validate_inner_is_simple_subclass`.  
The first checks inheritance; this one checks that the class is not the root itself.
"""