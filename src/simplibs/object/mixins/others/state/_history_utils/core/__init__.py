from .find_snapshot import find_snapshot
from .record_state import record_state
from .set_history_limit import set_history_limit


_DESIGN_NOTES = """
# Core History Utilities

## Purpose
Provides the foundational helper functions used by the History mixin.
These utilities implement the core mechanics of:

- snapshot lookup,
- snapshot recording,
- history limit enforcement.

They form the backbone of the history subsystem and are used by navigation,
diffing, import/export, and debugging tools.

## Components

| Component            | Type     | Description                                               |
| :--------------------| :--------| :-------------------------------------------------------- |
| `find_snapshot`      | Function | Resolves index or timestamp into a snapshot tuple.        |
| `record_state`       | Function | Creates and stores a new history entry.                   |
| `set_history_limit`  | Function | Enforces and applies the maximum history size.            |

## Notes
- These utilities are internal and not part of the public API.
- They are treated as core invariants of the history subsystem.
- All structural logic is delegated to History internals and SnapshotMixin.
"""
