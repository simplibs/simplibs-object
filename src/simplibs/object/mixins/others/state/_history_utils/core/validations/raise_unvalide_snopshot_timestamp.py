from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.state import HistoryProtocol


def raise_unvalide_snopshot_timestamp(
    instance: "HistoryProtocol",
    ref: Any,
) -> NoReturn:
    """
    Raises an error when a timestamp reference does not match any snapshot
    recorded in history.
    """
    # noinspection PyProtectedMember
    history_timestamps = tuple(ts for ts, _ in instance._history)

    raise SimpleRuntimeError(
        error_name="HISTORY SNAPSHOT TIMESTAMP ERROR",
        label="snapshot timestamp",
        expected="A timestamp that exists in recorded history.",
        value=ref,
        problem=(
            "Snapshot with the provided timestamp was not found.",
            f"Timestamp {ref!r} does not match any recorded snapshot."
        ),
        context=(
            f"History lookup attempted on instance '{type(instance).__name__}'.",
            f"Available timestamps: {history_timestamps}"
        ),
        how_to_fix=(
            "Ensure the timestamp refers to an existing snapshot.",
            "Use `history` or `export_history_to_dict` to inspect available timestamps.",
            "Snapshot timestamps are stored exactly as datetime values."
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_unvalide_snopshot_timestamp

## Purpose
Raises a structured error when the user provides a valid datetime timestamp
that does not exist in the history list.

## Why this validation exists
History navigation by timestamp requires an exact match.  
If the timestamp is not present, the lookup cannot proceed and must fail
deterministically.

Failing early ensures:
- predictable navigation,
- clear diagnostics,
- safe snapshot restoration.

## Execution context
Used inside `find_snapshot` after scanning all recorded timestamps.  
It is triggered only when the timestamp is valid but not found.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""