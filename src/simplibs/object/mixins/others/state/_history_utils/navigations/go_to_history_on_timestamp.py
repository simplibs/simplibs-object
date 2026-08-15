from typing import TYPE_CHECKING
from datetime import datetime
# Outers
from ..core.validations import raise_unvalide_timestamp, raise_unvalide_snopshot_timestamp
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def go_to_history_on_timestamp(
    self: "HistoryProtocol",
    timestamp: datetime
) -> None:
    """
    Navigates to a specific history entry by timestamp and restores its snapshot.
    """

    # 1. Validate timestamp type
    if not isinstance(timestamp, datetime):
        raise_unvalide_timestamp(self, timestamp)

    # 2. Search for matching timestamp
    for i, (ts, snapshot) in enumerate(self._history):
        if ts == timestamp:
            self._history_index = i
            self._restore_snapshot(snapshot)
            return

    # 3. Timestamp not found
    raise_unvalide_snopshot_timestamp(self, timestamp)


_DESIGN_NOTES = """
# go_to_history_on_timestamp

## Purpose
Navigates to a specific history entry using a datetime timestamp and restores
the corresponding snapshot. This function provides semantic, human‑readable
navigation within the history list.

## Architectural role
`go_to_history_on_timestamp` is used by:

- `History.go_to_timestamp`
- debugging tools
- diffing utilities
- history import/export pipelines
- composite and constant recalculation pipelines (when navigating snapshots)

It is the primary mechanism for timestamp‑based history navigation.

## How it works
The function performs three deterministic steps:

### 1. Validate timestamp
Ensures the provided value is a valid `datetime` instance.  
Invalid values trigger a structured validation error.

### 2. Search for matching timestamp
Iterates through the history list and compares timestamps.  
If a match is found:
- `_history_index` is updated,
- the snapshot is restored using `_restore_snapshot`,
- navigation completes immediately.

### 3. Timestamp not found
If no entry matches the provided timestamp, a structured validation error is
raised, including a list of available timestamps for debugging.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_index`, `_history_count`

- **SnapshotMixin**  
  Provides `_restore_snapshot(snapshot)`.

Without these components, timestamp‑based navigation cannot operate correctly.

## Why this function exists
Timestamp‑based navigation is:

- human‑friendly,
- semantically meaningful,
- ideal for debugging and diffing,
- useful when index positions are unknown or irrelevant.

This function encapsulates the minimal logic required to jump to a specific
historical moment.

## Deterministic behavior
Navigation is guaranteed to be:

- timestamp‑safe,
- stable across mutations,
- consistent with undo/redo semantics,
- compatible with diffing and debugging tools.

## Stability guarantee
Any change to this function would affect:

- navigation correctness,
- undo/redo behavior,
- snapshot restoration,
- debugging tools.

Therefore, `go_to_history_on_timestamp` is treated as a **core invariant** of
the history subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals and snapshot restoration.
"""
