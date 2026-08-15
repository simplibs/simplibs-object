from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def raise_history_limit_not_positive_integer(
    instance: "HistoryProtocol",
    value: object,
) -> NoReturn:
    """
    Raises an error when the provided history limit is not a positive integer.
    """

    raise SimpleMixinError(
        error_name="HISTORY LIMIT ERROR",
        label="history limit",
        expected="A positive integer (value >= 1).",
        value=value,
        problem=(
            "Invalid history limit provided.",
            "History limit must be a positive integer greater than or equal to 1."
        ),
        context=(
            f"History limit assignment attempted on instance '{type(instance).__name__}'.",
            f"Provided value type: {type(value).__name__}"
        ),
        how_to_fix=(
            "Ensure the limit is an integer.",
            "Ensure the limit is at least 1.",
            "Example valid values: 1, 5, 10, 100."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_history_limit_not_positive_integer

## Purpose
Raises a structured error when the user attempts to set a history limit that is
not a positive integer.

Valid values must satisfy:
`isinstance(value, int) and value >= 1`.

## Why this validation exists
History limit controls memory usage and navigation behavior.  
Invalid values could break history truncation logic or produce inconsistent
state.

Failing early ensures:
- predictable history behavior,
- safe truncation,
- clear diagnostics.

## Execution context
Used inside `set_history_limit` before applying the new limit.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""