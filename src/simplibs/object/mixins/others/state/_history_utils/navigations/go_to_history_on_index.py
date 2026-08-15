from typing import TYPE_CHECKING
# Outers
from ..core.validations import raise_unvalide_snapshot_index
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def go_to_history_on_index(
    self: "HistoryProtocol",
    index: int
) -> None:
    """
    Navigates to a specific history entry by index and restores its snapshot.
    """

    # 1. Validate index
    if not (0 <= index < self._history_count):
        raise_unvalide_snapshot_index(self, index)

    # 2. Switch to the selected entry
    self._history_index = index
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)


_DESIGN_NOTES = """
# go_to_history_on_index

## Purpose
Navigates to a specific history entry using its integer index and restores the
corresponding snapshot. This function provides fast, deterministic navigation
within the history list.

## Architectural role
`go_to_history_on_index` is used by:

- `History.go_to_index`
- undo/redo logic (indirectly)
- debugging tools
- diffing utilities
- composite and constant recalculation pipelines (when navigating snapshots)

It is the primary mechanism for index‑based history navigation.

## How it works
The function performs two deterministic steps:

### 1. Validate index
Ensures the index is within the valid range `[0, _history_count)`.  
Invalid indices trigger a structured validation error.

### 2. Restore snapshot
Updates `_history_index` and restores the snapshot using `_restore_snapshot`.
This operation mutates the instance to reflect the historical state.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_index`, `_history_count`

- **SnapshotMixin**  
  Provides `_restore_snapshot(snapshot)`.

Without these components, index‑based navigation cannot operate correctly.

## Why this function exists
Index‑based navigation is:

- fast,
- predictable,
- stable,
- independent of timestamps,
- ideal for undo/redo operations.

This function encapsulates the minimal logic required to jump to a specific
history entry.

## Deterministic behavior
Navigation is guaranteed to be:

- index‑safe,
- stable across mutations,
- consistent with undo/redo semantics,
- compatible with diffing and debugging tools.

## Stability guarantee
Any change to this function would affect:

- undo/redo behavior,
- navigation correctness,
- snapshot restoration,
- debugging tools.

Therefore, `go_to_history_on_index` is treated as a **core invariant** of the
history subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals and snapshot restoration.
"""
