from typing import Any
# Outers
from ....exceptions import SimpleRuntimeError


def validate_retries_is_int(
    retries: Any
) -> None:
    """Validates that the retries parameter is an instance of int (and not bool).

    Args:
        retries: Candidate retries argument to validate.

    Raises:
        SimpleRuntimeError: If retries is not an integer or is a boolean.
    """

    if isinstance(retries, int) and not isinstance(retries, bool):
        return

    raise SimpleRuntimeError(
        error_name="INVALID RETRIES TYPE ERROR",
        label="retries",
        expected="An integer instance representing attempt count.",
        value=type(retries).__name__,
        problem=(
            "Retries parameter must be an integer.",
            f"Received type '{type(retries).__name__}' instead of 'int'."
        ),
        context=(
            f"Received argument: {retries!r}",
        ),
        how_to_fix=(
            "Pass an integer value for retries, e.g. retries=5.",
            "Do not pass floats, strings, or boolean flags as retries."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_retries_is_int

## Purpose
Validates that `retries` is strictly an `int` (filtering out `bool`, as `bool` inherits from `int` in Python).

## Why this validation exists
Guarantees correct loop execution types.
"""