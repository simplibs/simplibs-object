from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
if TYPE_CHECKING:
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_method_is_callable(
    raw_method: Any,
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates that a class attribute is a callable object.

    Raises:
        SimpleMetadataError: If the raw attribute is not a callable object.
    """

    # 1. Structural evaluation checkpoint
    if not callable(raw_method):

        # 2. Extract shared diagnostic elements from context dictionary
        class_name = base_info["class_name"]
        method_name = base_info["method_name"]
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Method is not a callable object",
            expected="Callable class method definition.",
            problem=f"'{class_name}.{method_name}' is not callable.",
            context=context,
            how_to_fix=(
                f"Ensure that '{method_name}' is properly defined as a function hook.",
                "Verify that the method identifier has not been overwritten by a plain data attribute."
            ) + expected_structure,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_method_is_callable

## Purpose
Enforces operational invocation capability on reflected class attributes before signature auditing. It prevents early interpreter failures by ensuring that the targeted attribute descriptor is a valid callable rather than a static data field.

## Diagnostic Layout & Formatting
1. **Dictionary Integration**: Resolves dynamic interpolation fields (`class_name`, `method_name`) directly from the shared `base_info` context map. It utilizes the `"expected_structure"` token to dynamically chain the contextual structural blueprint snippet to the exception message.
2. **Defensive Reflection Guard**: Intercepts structural type corruptions at the boundary layer, ensuring that subsequent reflection routines can safely assume callable bytecode interfaces.
3. **Happy Path Performance**: Minimizes operational friction by executing a native `callable()` evaluation. If the assertion passes, it bypasses dictionary lookups and dictionary unpacking overhead entirely.
"""