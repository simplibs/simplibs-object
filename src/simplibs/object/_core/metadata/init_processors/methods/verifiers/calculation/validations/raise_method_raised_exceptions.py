from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleDefinitionError
from ..._exceptions_helpers import exception_info_for_classmethod
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def raise_method_raised_exceptions(
    intercepted_exception: Exception,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Raises a structured metadata exception when a dry-run execution fails."""

    # 1. Extract diagnostic context
    class_name, method_name, context = exception_info_for_classmethod(bound_method)

    # 2. Raise domain exception with packaged underlying error
    raise SimpleDefinitionError(
        error_name="METHOD LOGIC ERROR",
        label="_exception",
        expected="Method execution without raising exceptions.",
        problem="An unexpected error occurred during dry-run execution.",
        context=context,
        how_to_fix=(
            f"Inspect the internal logic of '{method_name}'.",
            "Verify correct handling of default values and input parameters.",
            "See the intercepted exception below for the exact root cause.",
        ),
        exception=intercepted_exception,
    )



_DESIGN_NOTES = """
# raise_method_raised_exceptions

## Purpose
Captures any exception thrown during a dry-run execution of a classmethod and
repackages it into a structured `SimpleDefinitionError`.  
This prevents raw runtime crashes from leaking into the metadata pipeline.

## Behavior
1. Extracts diagnostic context using `exception_context_for_classmethod`.
2. Raises a structured domain error containing:
   - class name
   - method name
   - execution context
   - remediation instructions
   - the original intercepted exception

## Notes
This validator is used exclusively inside `verify_calculation` and is the first
line of defense against runtime failures in method hooks.
"""