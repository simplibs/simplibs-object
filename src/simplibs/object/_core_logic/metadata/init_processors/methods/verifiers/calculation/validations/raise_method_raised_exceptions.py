from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from ..._exceptions_helpers import exception_context_for_classmethod
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol


def raise_method_raised_exceptions(
    intercepted_exception: Exception,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Raises a packaged metadata exception when a dry-run execution of a method fails with an error.

    Raises:
        SimpleMetadataError: Always, packaging the caught exception as the underlying cause.
    """

    # 0. Exception condition boundary
    # if intercepted_exception:

    # 1. Compute dynamic diagnostic variables
    class_name, method_name, context = exception_context_for_classmethod(bound_method)

    # 2. Raise domain exception with full packed diagnostic payload
    raise SimpleMetadataError(
        error_name="METHOD LOGIC ERROR",
        label="Exception during dry-run execution",
        expected="Successful completion of the calculation without raising any exceptions.",
        problem="An unexpected error occurred during the trial calculation run.",
        context=context,
        how_to_fix=(
            f"Check the internal implementation logic of the '{method_name}' method.",
            "Verify whether the method correctly processes its fallback default parameter values.",
            "The precise root cause of the failure is detailed below under 'Intercepted exception'."
        ),
        exception=intercepted_exception
    )


_DESIGN_NOTES = """
# raise_method_raised_exceptions

## Purpose
Acts as a dedicated panic handler that captures raw runtime crashes thrown during metadata dry-runs. It repackages unhandled operational errors into structured domain exceptions, ensuring that custom internal bugs do not break structural composition pipelines silently.

## Diagnostic Layout & Formatting
1. **Trace Interception**: Preserves the structural cause by nesting the raw `intercepted_exception` instance directly inside the `SimpleMetadataError` payload structure.
2. **Dynamic Reflection**: Reuses standard dynamic identifier fields extracted by `exception_context_for_classmethod` to dynamically isolate the exact class and classmethod origin locations.
3. **No-Bypass Execution**: As a pure error-path sink, this function bypasses conditional checking and completely offloads execution formatting and exception allocation costs from the main operational runtime flow.
"""