from typing import TYPE_CHECKING, NoReturn
# Outers
from .......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.state import HistoryProtocol


def raise_unvalide_snapshot_index(
    instance: "HistoryProtocol",
    ref: int,
) -> NoReturn:
    """
    Raises an error when a snapshot index is outside the valid range.
    """
    # noinspection PyProtectedMember
    history_count = instance._history_count

    raise SimpleRuntimeError(
        error_name="HISTORY SNAPSHOT INDEX ERROR",
        label="snapshot index",
        expected=f"Integer in range 0 <= index < {history_count}",
        value=ref,
        problem=(
            "Invalid snapshot index provided.",
            f"Index {ref} is outside the valid range of recorded history."
        ),
        context=(
            f"History lookup attempted on instance '{type(instance).__name__}'.",
            f"Total number of snapshots: {history_count}"
        ),
        how_to_fix=(
            "Ensure the index refers to an existing snapshot.",
            "Use `history_index` or inspect `history` to determine valid indices.",
            "Snapshot indices start at 0 and increase sequentially."
        ),
        exception=IndexError,
    )


_DESIGN_NOTES = """
# raise_unvalide_snapshot_index

## Purpose
Raises a structured error when the user provides a snapshot index that does not
exist in the history list.

Snapshot indices must satisfy:
`0 <= index < history_count`.

## Why this validation exists
History navigation relies on deterministic indexing.  
Invalid indices would lead to undefined behavior or incorrect snapshot access.

Failing early ensures:
- predictable navigation,
- safe snapshot restoration,
- clear diagnostics for debugging.

## Execution context
Used inside `find_snapshot` when the reference is an integer.  
It is the first validation step before returning the snapshot.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the History mixin.
"""