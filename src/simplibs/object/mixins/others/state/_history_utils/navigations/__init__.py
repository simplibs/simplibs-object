from .go_to_history_on_index import go_to_history_on_index
from .go_to_history_on_timestamp import go_to_history_on_timestamp
from .go_to_last_history import go_to_last_history
from .history_redo import history_redo
from .history_undo import history_undo


_DESIGN_NOTES = """
# History Navigation Utilities

## Purpose
Provides navigation helpers used by the History mixin to move between
historical snapshots. These utilities implement the core mechanics of:

- index-based navigation,
- timestamp-based navigation,
- undo/redo traversal,
- jumping to the latest state.

They form the operational layer of the history subsystem and are used by
debugging tools, diffing utilities, import/export pipelines, and interactive
editing workflows.

## Components

| Component                    | Type     | Description                                              |
| :--------------------------- | :--------| :------------------------------------------------------- |
| `go_to_history_on_index`     | Function | Navigates to a specific history entry by index.          |
| `go_to_history_on_timestamp` | Function | Navigates to a specific history entry by timestamp.      |
| `go_to_last_history`         | Function | Jumps to the most recent history entry.                  |
| `history_redo`               | Function | Moves forward to the next history entry.                 |
| `history_undo`               | Function | Moves backward to the previous history entry.            |

## Notes
- These utilities are internal and not part of the public API.
- They rely on History internals and SnapshotMixin for state restoration.
- They are treated as core invariants of the history subsystem.
"""
