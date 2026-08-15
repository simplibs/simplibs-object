from typing import TYPE_CHECKING, Any
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_inners_is_not_empty(
    inners: Any,
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that '_inners' is not an empty tuple."""

    # 1. Check emptiness
    if not (isinstance(inners, tuple) and not inners):
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Raise error
    raise SimpleDefinitionError(
        error_name=error_name,
        label="_inners_empty",
        expected="Non-empty tuple of SimpleConstant / SimpleObject subclasses",
        value=inners,
        problem=f"Class '{class_name}' defines '_inners' as an empty tuple.",
        context=context,
        how_to_fix=(
            "Remove '_inners' entirely if the class has no inner components.",
            "If this is a composition, define at least one inner element.",
        ) + acceptable,
        exception=ValueError,
    )


_DESIGN_NOTES = """
# validate_inners_is_not_empty

## Purpose
Ensures that `_inners` is not an empty tuple.  
If a class declares `_inners`, it must contain at least one inner element.

## Behavior
1. Checks whether `_inners` is an empty tuple.
2. If empty, retrieves shared diagnostic info.
3. Raises a structured `SimpleDefinitionError`.

## Notes
An empty `_inners` is semantically invalid:
- a class with no inners should behave as a constant,
- a composition must declare at least one inner.

"""