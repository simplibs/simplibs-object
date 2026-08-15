# Outers
from ....exceptions import SimpleLogicError


def validate_retries_is_greater_than_zero(
    retries: int
) -> None:
    """Validates that the retries count is an integer strictly greater than zero.

    Args:
        retries: Numeric retries attempt count to validate.

    Raises:
        SimpleLogicError: If retries <= 0.
    """

    if retries > 0:
        return

    raise SimpleLogicError(
        error_name="INVALID RETRIES BOUNDS ERROR",
        label="retries",
        expected="An integer strictly greater than 0 (e.g. 1, 5, 10).",
        value=retries,
        problem=(
            "Retries parameter must be a positive non-zero integer.",
            f"Received value {retries}, which allows zero attempts for value generation."
        ),
        context=(
            f"Configured retries count: {retries}",
        ),
        how_to_fix=(
            "Provide a retries value >= 1 (default recommended is 5).",
            "Do not pass zero or negative numbers as retries count."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# validate_retries_is_greater_than_zero

## Purpose
Validates that `retries` is positive (> 0).

## Why this validation exists
A retry count of 0 or negative would prevent `range(retries)` from executing even a single generation attempt.
"""