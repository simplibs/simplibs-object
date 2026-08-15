from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def raise_unexpected_validation_error(
    cls: "SimpleConstantProtocol",
    value: Any,
    original_exception: Exception,
) -> NoReturn:
    """Raises a standardized error when user-defined validation fails unexpectedly."""

    class_name = cls.__name__

    raise SimpleLogicError(
        error_name="VALIDATION ERROR",
        label="value",
        value=value,
        expected="A value that satisfies the user-defined validation logic.",
        problem=(
            f"The value could not be validated successfully.",
            f"An unexpected exception occurred during validation in '{class_name}'. "
        ),
        context=(
            f"The validation pipeline for '{class_name}' intercepted an exception "
            f"raised inside the user-defined '_validate' method. ",
            f"This may indicate either an invalid value or an internal error in the validation logic."
        ),
        how_to_fix=(
            "Review the intercepted exception shown at the end of this error message "
            "to determine whether the issue is caused by invalid input or a bug in "
            "the '_validate' method.",
            "If you intend to raise custom validation errors, ensure they inherit "
            "from 'SimpleObjectError' so they are handled as expected.",
            "If the error is unintended, verify that the validation logic does not "
            "perform unsafe operations or rely on assumptions that may not hold."
        ),
        exception=original_exception,
    )


_DESIGN_NOTES = """
# raise_unexpected_validation_error

## Purpose
Handles any unexpected exception raised during user-defined validation (`_validate`).
This error is user-facing and explains that validation failed due to an internal
exception rather than a structured validation error.

## Behavior
- Triggered when `_validate` raises an exception that is **not** a `SimpleObjectError`.
- Wraps the original exception into a structured `SimpleLogicError`.
- Provides clear guidance for both possible scenarios:
  1. The value is invalid and caused the user’s validation logic to fail.
  2. The validation logic itself contains an error.

## Notes
- The original exception is preserved and displayed under “Intercepted exception”
  in the formatted error output.
- If the user intends to raise custom validation errors, they should inherit from
  `SimpleObjectError` so they are treated as expected validation failures.
- This function ensures consistent error formatting across all validation paths.
"""