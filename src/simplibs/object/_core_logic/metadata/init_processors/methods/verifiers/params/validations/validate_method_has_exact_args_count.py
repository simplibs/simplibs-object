from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ..._exceptions_helpers import ClassMethodExceptionInfoPayload


def validate_method_has_exact_args_count(
    expected_args_count: int,
    actual_args_count: int,
    base_info: "ClassMethodExceptionInfoPayload",
) -> None:
    """Validates the exact count of positional arguments against the compiled function bytecode.

    Raises:
        SimpleMetadataError: If the actual positional argument count does not match the expected count.
    """

    # 1. Structural evaluation checkpoint
    if actual_args_count != expected_args_count:

        # 2. Extract shared diagnostic elements from context dictionary
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Raise domain exception with full packed diagnostic payload
        raise SimpleMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            label="Incorrect number of positional arguments",
            expected=f"Positional arguments count: {expected_args_count}",
            problem=f"Received positional arguments count: {actual_args_count}",
            context=context,
            how_to_fix=(
                "Check whether you declared all required positional parameters after the 'cls' token.",
                "Verify that your classmethod signature strictly matches the required framework definition."
            ) + expected_structure,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_method_has_exact_args_count

## Purpose
Enforces strict positional argument counts on custom classmethods (`_validate`, `_logic`, `_decompose`). It explicitly checks `co_argcount` from Python's internal function bytecode layer before executing the method.

## Diagnostic Layout & Formatting
1. **Dictionary Integration**: Seamlessly extracts formatting parameters from the shared `base_info` payload map populated by `exception_info_for_classmethod`. It explicitly uses the `"expected_structure"` tracking token to integrate the copy-paste remediation snippet.
2. **Bytecode-Level Verification**: By matching integer counts before invocation, the framework captures misconfigured definitions without risking side effects from running an invalid function blueprint.
3. **Happy Path Performance**: Evaluates a single native integer inequality comparison. If arguments match, execution bypasses dictionary lookups and exits instantly.
"""