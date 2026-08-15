from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.state import HistoryProtocol


def history_undo(
    self: "HistoryProtocol"
) -> bool:
    """
    Moves backward to the previous history entry (if available) and restores its snapshot.
    """

    # 1. Check if a backward move is possible
    if self._history_index <= 0:
        return False

    # 2. Move to the previous entry
    self._history_index -= 1
    _, snapshot = self._history[self._history_index]
    self._restore_snapshot(snapshot)
    return True


_DESIGN_NOTES = """
# history_undo

## Purpose
Moves backward in the history list and restores the snapshot of the previous
entry. This function implements the backward half of the undo/redo navigation
model.

## Architectural role
`history_undo` is used by:

- `History.undo`
- interactive editing workflows
- debugging tools
- composite and constant recalculation pipelines
- history import/export routines (when replaying state transitions)

It provides deterministic backward navigation within the history subsystem.

## How it works
The function performs two deterministic steps:

### 1. Check if backward navigation is possible
If the current index already points to the first history entry, the function
returns `False` and performs no action.  
This prevents invalid navigation and avoids unnecessary snapshot restoration.

### 2. Restore the previous snapshot
If navigation is possible:
- `_history_index` is decremented,
- the snapshot of the previous entry is restored using `_restore_snapshot`,
- the function returns `True` to signal successful navigation.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_index`, `_history_count`

- **SnapshotMixin**  
  Provides `_restore_snapshot(snapshot)`.

Without these components, undo navigation cannot operate correctly.

## Why this function exists
Undo/redo navigation is a core feature of:

- interactive editing,
- state debugging,
- reversible transformations,
- history replay,
- composite recalculation.

`history_undo` encapsulates the minimal logic required to move backward safely
and deterministically.

## Deterministic behavior
Undo navigation is guaranteed to be:

- index‑safe,
- stable across mutations,
- consistent with redo semantics,
- compatible with diffing and debugging tools.

## Stability guarantee
Any change to this function would affect:

- undo/redo behavior,
- navigation correctness,
- snapshot restoration,
- debugging tools.

Therefore, `history_undo` is treated as a **core invariant** of the history
subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals and snapshot restoration.
"""
