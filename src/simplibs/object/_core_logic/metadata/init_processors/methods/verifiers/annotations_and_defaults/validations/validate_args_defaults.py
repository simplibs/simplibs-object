from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_args_defaults(
    expected_args_defaults: tuple[Any, ...],
    expected_params: tuple[str, ...],
    bound_method: "ClassMethodProtocol",
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that the default values of positional arguments strictly match the defaults defined in '_inners'.

    In the Simple framework, defaults are deterministic and derived directly from metadata.
    The user must not alter them – they can only be completely omitted from the signature.

    Raises:
        SimpleMetadataError: If any explicitly defined positional default value mismatches the blueprint schema.
    """

    # 1. Extract explicitly declared user defaults from the target positional arguments
    method_args_defaults = bound_method.__func__.__defaults__ or ()

    # 2. If the user provided no signatures defaults, exit immediately (Happy Path)
    if not method_args_defaults:
        return

    # 3. Iterate over signature parameters and verify structural value equality
    for index, (value, expected_value) in enumerate(zip(method_args_defaults, expected_args_defaults)):
        if value != expected_value:

            # 3.1 Extract shared pre-computed diagnostic elements from base payload
            expected_structure = base_info["expected_structure"]
            context = base_info["context"]
            param_name = expected_params[index]

            # 3.2 Raise domain exception with full packed diagnostic payload
            raise SimpleMetadataError(
                error_name="METHOD SIGNATURE ERROR",
                label="Invalid argument default value",
                expected=f"No default value or a value conforming to the '_inners' definition: '{expected_value}'",
                value=value,
                problem=f"Parameter '{param_name}' has an incorrect default value.",
                context=context,
                how_to_fix=(
                    f"Align the default value of parameter '{param_name}' with its definition inside '_inners'.",
                    f"Recommended value: {repr(expected_value)}",
                    "Alternatively, remove the default value from the method signature entirely;",
                    "the framework will automatically inject it during metadata initialization.",
                ) + expected_structure,
                exception=ValueError
            )


_DESIGN_NOTES = """
# validate_args_defaults

## Purpose
Enforces strict value synchronization between user-defined standard positional argument defaults (`__defaults__`) and the immutable internal metadata configuration patterns of the framework. It prevents drift between static signature boilerplate documentation and actual runtime evaluation states.

## Diagnostic Layout & Formatting
1. **Index-Based Parameter Resolution**: Performs a synchronized traversal over zip collections, utilizing the loop index indicator to capture the correct positional variable name from `expected_params` for accurate error attribution.
2. **Immutable Blueprint Merging**: Smoothly concatenates pre-rendered boilerplate layout markers from `base_info["expected_structure"]` straight into the diagnostic report's `how_to_fix` data block using tuple arithmetic.
3. **Happy Path Performance**: Protects core initialization tasks by utilizing a cheap short-circuit check on `method_args_defaults`. For methods leaving argument initialization tasks entirely to internal framework control, loop checking and memory expansion costs are completely skipped.
"""