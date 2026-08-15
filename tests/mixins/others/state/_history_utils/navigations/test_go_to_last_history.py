from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.state import HistoryProtocol


def go_to_last_history(
    self: "HistoryProtocol"
) -> None:
    """
    Navigates to the last history entry and restores its snapshot.
    """

    # 1. Check if already at the last entry
    last_index = self._history_count - 1
    if self._history_index != last_index:

        # 2. Switch to the last entry
        self._history_index = last_index
        _, snapshot = self._history[self._history_index]
        self._restore_snapshot(snapshot)


_DESIGN_NOTES = """
# go_to_last_history

## Purpose
Navigates to the most recent history entry and restores its snapshot.  
This function provides a fast, deterministic way to jump to the newest state
recorded in the history subsystem.

## Architectural role
`go_to_last_history` is used by:

- `History.go_to_last`
- debugging tools
- diffing utilities
- composite and constant recalculation pipelines
- import/export routines (when restoring history)

It is the primary mechanism for “jump to latest state” navigation.

## How it works
The function performs two deterministic steps:

### 1. Check if navigation is needed
If the current history index already points to the last entry, the function
performs no action. This avoids unnecessary snapshot restoration.

### 2. Restore the last snapshot
If navigation is needed:
- `_history_index` is updated,
- the snapshot of the last entry is restored using `_restore_snapshot`.

This mutates the instance to reflect the most recent historical state.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_index`, `_history_count`

- **SnapshotMixin**  
  Provides `_restore_snapshot(snapshot)`.

Without these components, last‑entry navigation cannot operate correctly.

## Why this function exists
Jumping to the latest state is a common operation in:

- debugging,
- interactive editing,
- undo/redo workflows,
- history import/export,
- composite recalculation.

This function encapsulates the minimal logic required to perform that jump
safely and deterministically.

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

Therefore, `go_to_last_history` is treated as a **core invariant** of the
history subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals and snapshot restoration.
"""
