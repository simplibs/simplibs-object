from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def raise_unvalide_timestamp(
    instance: "HistoryProtocol",
    ref: object,
) -> NoReturn:
    """
    Raises an error when the provided timestamp reference is not a valid datetime.
    """

    raise SimpleMixinError(
        error_name="HISTORY TIMESTAMP ERROR",
        label="timestamp",
        expected="A valid datetime object.",
        value=type(ref).__name__,
        problem=(
            "Invalid timestamp reference provided.",
            "History lookup requires a datetime value."
        ),
        context=(
            f"History lookup attempted on instance '{type(instance).__name__}'.",
            f"Provided value type: {type(ref).__name__}"
        ),
        how_to_fix=(
            "Ensure the reference is a datetime object.",
            "Use `go_to_timestamp` or `find_snapshot` with a valid datetime.",
            "Do not pass integers, strings, or other types."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_unvalide_timestamp

## Purpose
Raises a structured error when the user provides a timestamp reference that is
not a valid `datetime` object.

## Why this validation exists
History navigation by timestamp requires an exact datetime match.  
Passing any other type (string, int, float, None, etc.) would make the lookup
ambiguous or meaningless.

Failing early ensures:
- predictable timestamp navigation,
- clear diagnostics,
- safe snapshot restoration.

## Execution context
Used inside `find_snapshot` when the reference is expected to be a datetime.
It is the first validation step before searching for a matching timestamp.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""