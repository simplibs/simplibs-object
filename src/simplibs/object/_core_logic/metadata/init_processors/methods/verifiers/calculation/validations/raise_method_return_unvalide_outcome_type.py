from typing import Any, TYPE_CHECKING
from types import UnionType
# Outers
from ........exceptions import SimpleMetadataError
from ..._exceptions_helpers import exception_context_for_classmethod

# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol


def raise_method_return_unvalide_outcome_type(
    calculated_value: Any,
    expected_return_type: type | UnionType,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Raises an exception when the return value from a trial calculation does not match the expected type.

    Raises:
        SimpleMetadataError: Always, as this is a dedicated exception raiser.
    """

    # 0. Exception condition boundary
    # if not isinstance(calculated_value, expected_return_type):

    # 1. Compute dynamic diagnostic variables and fallback typenames
    class_name, method_name, context = exception_context_for_classmethod(bound_method)

    expected_type_name = expected_return_type.__name__ if hasattr(expected_return_type, "__name__") else str(expected_return_type)
    calculated_type_name = type(calculated_value).__name__

    type_definition = {
        "_logic": f"The return value should correspond to the definition of '{class_name}._type'.",
        "_decompose": f"The return value must be a tuple matching the element count and item types defined in '{class_name}._inners'.",
        "_validate": "The return value must be 'bool', 'None', or a union layout 'bool | None'."
    }

    # 2. Raise domain exception with full packed diagnostic payload
    raise SimpleMetadataError(
        error_name="METHOD LOGIC ERROR",
        label="Invalid calculation outcome type",
        expected=f"Return value of type '{expected_type_name}'.",
        value=calculated_value,
        problem=f"The outcome of method '{method_name}' does not match the defined type blueprint.",
        context=context,
        how_to_fix=(
            "The error may be caused by the method logic itself, or by the schema definition used to verify the method.",
            f"{type_definition.get(method_name, '')}",
            f"Either modify the method logic so that it explicitly returns a '{expected_type_name}' instance.",
            f"Or update the target type definition schema to accommodate the calculated type '{calculated_type_name}'.",
            "Example:",
            "    @classmethod",
            f"    def {method_name}(cls, ...) -> {expected_type_name}:",
            f"        return ...  # Must be an instance of {expected_type_name}"
        ),
        exception=TypeError
    )


_DESIGN_NOTES = """
# raise_method_return_unvalide_outcome_type

## Purpose
Acts as a centralized diagnostic error checkpoint when a trial evaluation run of a standard classmethod (`_logic`, `_decompose`, or `_validate`) yields a return value type mismatch against the pre-compiled type metadata configuration schema.

## Diagnostic Layout & Formatting
1. **Dynamic Context Routing**: Selects localized remediation string hints from a static dictionary layout using the current method name token as a key, providing specific context for each architectural layer.
2. **Union-Safe Type Introspection**: Extracts type string signatures safely, preventing internal interpreter crashes when dealing with complex runtime expressions such as `types.UnionType` or pipe types.
3. **No-Bypass Execution**: Because this function handles the error state exclusively, it skips condition tracking and drops directly into string composition and exception allocation routines to offload the main execution path.
"""