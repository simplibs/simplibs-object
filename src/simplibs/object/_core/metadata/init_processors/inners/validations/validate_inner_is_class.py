from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_inner_is_class(
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that an inner element is a class."""

    # 1. Check type
    if isinstance(inner, type):
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Raise error
    raise SimpleDefinitionError(
        error_name=error_name,
        label="inner_not_class",
        expected="Class inheriting from SimpleConstant or SimpleObject",
        value=inner,
        problem=f"Inner element '{inner}' inside '{inners}' is not a class.",
        context=context,
        how_to_fix=(
            "Use class references, not instances.",
            "Example: MyElement, not MyElement().",
            "Ensure the item is not a string or primitive value.",
        ) + acceptable,
        exception=TypeError,
    )



_DESIGN_NOTES = """
# validate_inner_is_class

## Purpose
Ensures that each element in `_inners` is a class, not an instance or primitive.

## Behavior
1. Checks whether the inner element is a `type`.
2. If invalid, retrieves shared diagnostic info.
3. Raises a structured `SimpleDefinitionError`.

## Notes
This validator prevents accidental instantiation in `_inners`, such as writing
`MyElement()` instead of `MyElement`.

"""