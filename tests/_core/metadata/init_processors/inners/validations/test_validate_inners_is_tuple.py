from typing import TYPE_CHECKING, Any
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_inners import _exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_inners_is_tuple(
    inners: Any,
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that '_inners' is a tuple."""

    # 1. Check type
    if isinstance(inners, tuple):
        return

    # 2. Diagnostic info
    class_name, error_name, context, acceptable = _exception_info_for_inners(owner_class)

    # 3. Raise error
    raise SimpleMetadataError(
        error_name=error_name,
        label="_inners_not_tuple",
        expected="Tuple of SimpleConstant / SimpleObject subclasses",
        value=inners,
        problem=f"Class '{class_name}' defines '_inners' using an invalid type.",
        context=context,
        how_to_fix=(
            "Define '_inners' as a tuple.",
            "Example: _inners = (ElementA, ElementB)",
            "Single element requires a trailing comma: (ElementA,)",
        ) + acceptable,
        exception=TypeError,
    )



_DESIGN_NOTES = """
# validate_inners_is_tuple

## Purpose
Ensures that `_inners` is declared as a tuple. Tuples provide immutability and
preserve positional order, which is required for `_logic` signature generation.

## Behavior
1. Checks whether `_inners` is a tuple.
2. If invalid, retrieves shared diagnostic info.
3. Raises a structured `SimpleMetadataError`.

## Notes
This validator prevents accidental use of lists, sets, or missing trailing commas
in single-element tuple declarations.
"""