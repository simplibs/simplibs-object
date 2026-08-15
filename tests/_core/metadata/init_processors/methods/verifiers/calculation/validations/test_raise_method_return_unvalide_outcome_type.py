from typing import Any, TYPE_CHECKING
from types import UnionType
# Outers
from ........exceptions import SimpleMetadataError
from ..._exceptions_helpers import exception_info_for_classmethod
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def raise_method_return_unvalide_outcome_type(
    calculated_value: Any,
    expected_return_type: type | UnionType,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Raises a structured exception when a method returns an invalid type."""

    # 1. Extract diagnostic context
    class_name, method_name, context = exception_info_for_classmethod(bound_method)

    expected_type_name = (
        expected_return_type.__name__
        if hasattr(expected_return_type, "__name__")
        else str(expected_return_type)
    )
    calculated_type_name = type(calculated_value).__name__

    # 2. Select method-specific remediation hint
    if method_name == "_logic":
        hint = f"Return value must match '{class_name}._type'."
    elif method_name == "_decompose":
        hint = f"Return value must be a tuple matching '{class_name}._inners'."
    elif method_name == "_validate":
        hint = "Return value must be 'bool', 'None', or 'bool | None'."
    else:
        hint = ""

    # 3. Raise domain exception
    raise SimpleMetadataError(
        error_name="METHOD LOGIC ERROR",
        label="_return_type",
        value=calculated_value,
        expected=expected_type_name,
        problem=f"Method '{method_name}' returned an invalid type '{calculated_type_name}'.",
        context=context,
        how_to_fix=(
            "Inspect the method logic and ensure the returned value matches the expected type.",
            hint,
            f"Modify the method so that it returns an instance of '{expected_type_name}'.",
            f"Or update the type definition to allow '{calculated_type_name}'.",
            "Example:",
            "    @classmethod",
            f"    def {method_name}(cls, ...) -> {expected_type_name}:",
            f"        return ...  # Must be an instance of {expected_type_name}",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_method_return_unvalide_outcome_type

## Purpose
Ensures that the return value of `_logic`, `_decompose`, or `_validate` matches
the expected type defined by the metadata pipeline.

## Behavior
1. Extracts diagnostic context using `exception_context_for_classmethod`.
2. Determines the expected type name and the actual returned type.
3. Selects a method-specific remediation hint:
   - `_logic` → must match `_type`
   - `_decompose` → must match `_inners`
   - `_validate` → must be `bool | None`
4. Raises a structured `SimpleMetadataError` with a clear explanation and
   copy‑paste ready remediation instructions.

## Notes
This validator is used inside `verify_calculation` immediately after the dry-run
execution of the method.
"""