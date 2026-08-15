from typing import Any
# Outers
from ....exceptions import SimpleLogicError


def validate_skip_unregistered_is_bool(
    skip_unregistered: Any
) -> None:
    """Validates that skip_unregistered is a boolean flag.

    Args:
        skip_unregistered: Candidate argument to validate.

    Raises:
        SimpleLogicError: If skip_unregistered is not a bool.
    """
    if isinstance(skip_unregistered, bool):
        return

    raise SimpleLogicError(
        error_name="INVALID SKIP_UNREGISTERED TYPE ERROR",
        label="skip_unregistered",
        expected="A boolean value (True or False).",
        value=type(skip_unregistered).__name__,
        problem=(
            "skip_unregistered parameter must be a boolean flag.",
            f"Received type '{type(skip_unregistered).__name__}' instead of 'bool'."
        ),
        context=(
            f"Received argument: {skip_unregistered!r}",
        ),
        how_to_fix=(
            "Pass True or False for skip_unregistered.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_skip_unregistered_is_bool

## Purpose
Validates that `skip_unregistered` is a boolean flag.
"""