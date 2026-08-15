from typing import Any, TYPE_CHECKING
# Outers
from .........exceptions import SimpleDefinitionError
from ...._exceptions_helpers import exception_info_for_classmethod
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol
    from ........protocols.classes import SimpleClassLike


def validate_decompose_unvalide_item_value(
    value: Any,
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    bound_method: "ClassMethodProtocol",
) -> None:
    """Validates that a decomposed item matches its expected default value."""

    # 1. Structural evaluation checkpoint
    if value == inner.meta.default:
        return

    # 2. Extract diagnostic context
    class_name, method_name, context = exception_info_for_classmethod(bound_method)

    meta = inner.meta
    expected_value = meta.default

    inner_defaults = tuple(repr(i.meta.default) for i in inners)
    inner_names = tuple(i.meta.name_snake for i in inners)

    # 3. Raise domain exception
    raise SimpleDefinitionError(
        error_name="METHOD LOGIC ERROR",
        label="_decompose_item_value",
        value=value,
        expected=repr(expected_value),
        problem=f"Item '{meta.name_snake}' does not match its expected default value.",
        context=context,
        how_to_fix=(
            f"Ensure that '{meta.name_snake}' is computed as '{expected_value!r}'.",
            f"Received value: '{value!r}'.",
            "Verify that the returned tuple preserves the exact order defined in '_inners'.",
            f"Expected order: {', '.join(inner_names)}.",
            "Example based on default values:",
            f"    return ({', '.join(inner_defaults)})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# validate_decompose_unvalide_item_value

## Purpose
Ensures that each item returned by `_decompose` matches the default value defined
in the corresponding inner metadata (`inner.meta.default`).

## Behavior
1. Performs a fast equality check.
2. If the value is invalid:
   - extracts diagnostic context
   - determines expected default value
   - builds example default tuple
   - raises a structured `SimpleDefinitionError`

## Notes
This validator is used inside `verify_decompose_outcome` immediately after the
type validation.  
It is the final structural check for `_decompose` before returning the verified
tuple.
"""