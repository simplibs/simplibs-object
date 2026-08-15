from typing import Any, TYPE_CHECKING
from types import UnionType
# Outers
from .........exceptions import SimpleDefinitionError
from ...._exceptions_helpers import exception_info_for_classmethod
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol
    from ........protocols.classes import SimpleClassLike


def validate_decompose_unvalide_item_type(
    value: Any,
    expected_type: type | UnionType,
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    bound_method: "ClassMethodProtocol",
) -> None:
    """Validates that a decomposed item matches its expected type."""

    # 1. Structural evaluation checkpoint
    if isinstance(value, expected_type):
        return

    # 2. Extract diagnostic context
    class_name, method_name, context = exception_info_for_classmethod(bound_method)

    meta = inner.meta
    expected_type_name = (
        expected_type.__name__
        if hasattr(expected_type, "__name__")
        else str(expected_type)
    )

    inner_defaults = tuple(repr(i.meta.default) for i in inners)
    inner_names = tuple(i.meta.name_snake for i in inners)

    # 3. Raise domain exception
    raise SimpleDefinitionError(
        error_name="METHOD LOGIC ERROR",
        label="_decompose_item_type",
        value=value,
        expected=expected_type_name,
        problem=f"Item '{meta.name_snake}' does not match its expected type.",
        context=context,
        how_to_fix=(
            f"Ensure that '{meta.name_snake}' is computed as an instance of '{expected_type_name}'.",
            f"Received type: '{type(value).__name__}'.",
            "Verify that the returned tuple preserves the exact order defined in '_inners'.",
            f"Expected order: {', '.join(inner_names)}.",
            "Example based on default values:",
            f"    return ({', '.join(inner_defaults)})",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_decompose_unvalide_item_type

## Purpose
Ensures that each item returned by `_decompose` matches the expected type
defined in the corresponding inner metadata (`inner.meta.value_type`).

## Behavior
1. Performs a fast `isinstance` check.
2. If the value is invalid:
   - extracts diagnostic context
   - determines expected type name
   - builds example default tuple
   - raises a structured `SimpleDefinitionError`

## Notes
This validator is used inside `verify_decompose_outcome` immediately after the
length check.  
It is the first type-level validation before checking default-value compliance.
"""