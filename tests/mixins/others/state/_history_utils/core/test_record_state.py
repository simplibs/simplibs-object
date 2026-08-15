from typing import TYPE_CHECKING
from datetime import datetime
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.state import HistoryProtocol
    from ....._core.protocols.alias_typings import HistoryEntry


def record_state(
    self: "HistoryProtocol"
) -> "HistoryEntry":
    """
    Creates a snapshot of the current instance state and stores it in history.
    """

    # 1. Create timestamp and snapshot
    timestamp = datetime.now()
    snapshot = self._build_snapshot()

    # 2. Enforce history limit
    if self._history_limit and self._history_count >= self._history_limit:
        self._history.pop(0)

    # 3. Store entry
    history_entry = (timestamp, snapshot)
    self._history.append(history_entry)
    self._history_count = len(self._history)
    self._history_index = self._history_count - 1

    # 4. Return entry
    return history_entry


_DESIGN_NOTES = """
# record_state

## Purpose
Creates a new history entry representing the current state of the instance.
Each entry consists of a timestamp and a snapshot (tuple of raw node values).
This function is the foundation of the history subsystem: every state change,
initialization, or navigation ultimately relies on `record_state` to capture
the instance’s evolution over time.

## Architectural role
`record_state` is used by:

- History mixin initialization (`init_mixins`)
- automatic state tracking during mutations
- undo/redo navigation
- timestamp/index-based navigation
- history export/import pipelines
- debugging and diffing tools

It ensures that every relevant state transition is captured in a stable,
deterministic format.

## How it works
The function performs four deterministic steps:

### 1. Create timestamp and snapshot
Captures the current moment using `datetime.now()` and builds a raw snapshot
via `_build_snapshot()`.  
The snapshot is a tuple of values in the exact order of `_nodes_tuple`.

### 2. Enforce history limit
If a history limit is set and the history is full, the oldest entry is removed.
This ensures bounded memory usage and predictable history size.

### 3. Store entry
Creates a `(timestamp, snapshot)` tuple and appends it to the internal history
list. Updates:

- `_history_count` — total number of entries  
- `_history_index` — index of the most recent entry  

### 4. Return entry
Returns the newly created history entry for convenience and debugging.

## Integration requirements
The function assumes the instance implements:

- **SnapshotMixin**  
  Provides `_build_snapshot()`.

- **HistoryMixin internals**  
  Provides `_history`, `_history_limit`, `_history_index`, `_history_count`.

Without these components, the history subsystem cannot operate correctly.

## Why this function exists
History tracking must be:

- deterministic,
- lightweight,
- stable across mutations,
- independent of internal representation,
- safe for undo/redo navigation,
- compatible with serialization.

`record_state` encapsulates all of this in a single, minimal utility.

## Deterministic behavior
Each history entry is guaranteed to be:

- timestamped,
- structurally consistent,
- ordered,
- immutable,
- safe for navigation and diffing.

This determinism is essential for debugging, reproducibility, and state
management.

## Stability guarantee
Any change to this function would affect:

- undo/redo behavior,
- navigation correctness,
- history export/import,
- diffing tools,
- initialization behavior.

Therefore, `record_state` is treated as a **core invariant** of the history
subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to `_build_snapshot` and history internals.
"""
