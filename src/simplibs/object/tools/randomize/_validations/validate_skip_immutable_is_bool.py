from typing import Any
from ....exceptions import SimpleRuntimeError


def validate_skip_immutable_is_bool(
    skip_immutable: Any
) -> None:
    """Validates that skip_immutable is a boolean flag.

    Args:
        skip_immutable: Candidate argument to validate.

    Raises:
        SimpleRuntimeError: If skip_immutable is not a bool.
    """
    if isinstance(skip_immutable, bool):
        return

    raise SimpleRuntimeError(
        error_name="INVALID SKIP_IMMUTABLE TYPE ERROR",
        label="skip_immutable",
        expected="A boolean value (True or False).",
        value=type(skip_immutable).__name__,
        problem=(
            "skip_immutable parameter must be a boolean flag.",
            f"Received type '{type(skip_immutable).__name__}' instead of 'bool'."
        ),
        context=(
            f"Received argument: {skip_immutable!r}",
        ),
        how_to_fix=(
            "Pass True or False for skip_immutable.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_skip_immutable_is_bool

## Purpose
Validates that `skip_immutable` is a boolean flag.
"""