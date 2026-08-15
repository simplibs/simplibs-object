from typing import TYPE_CHECKING
from datetime import datetime
# Outers
from .validations import (
    raise_unvalide_snapshot_index,
    raise_unvalide_timestamp,
    raise_unvalide_snopshot_timestamp,
    raise_unvalide_snopshot_reference,
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.state import HistoryProtocol
    from ....._core.protocols.alias_typings import SnapshotTuple


def find_snapshot(
    self: "HistoryProtocol",
    ref: int | datetime
) -> "SnapshotTuple":
    """
    Resolves an index or timestamp reference into a snapshot tuple.
    """

    # 1. Handle integer reference
    if isinstance(ref, int):

        # 1.1 Validate index
        if not (0 <= ref < self._history_count):
            raise_unvalide_snapshot_index(self, ref)

        # 1.2 Return snapshot
        return self._history[ref][1]

    # 2. Handle datetime reference
    if isinstance(ref, datetime):

        # 2.1 Validate timestamp type
        if not isinstance(ref, datetime):
            raise_unvalide_timestamp(self, ref)

        # 2.2 Search for matching timestamp
        for ts, snapshot in self._history:
            if ts == ref:
                return snapshot

        # 2.3 Timestamp not found
        raise_unvalide_snopshot_timestamp(self, ref)

    # 3. Invalid reference type
    raise_unvalide_snopshot_reference(self, ref)


_DESIGN_NOTES = """
# find_snapshot

## Purpose
Resolves a snapshot reference — either an integer index or a datetime
timestamp — into the corresponding snapshot tuple stored in history.
This function is the central lookup mechanism of the history subsystem.

## Architectural role
`find_snapshot` is used by:

- `History.diff` (snapshot comparison)
- navigation utilities (`go_to_index`, `go_to_timestamp`)
- undo/redo logic
- debugging tools
- history export/import validation

It provides a deterministic way to retrieve historical state regardless of
whether the user references it by index or timestamp.

## How it works
The function performs three deterministic steps:

### 1. Integer reference
If `ref` is an integer:
- validates that the index is within bounds,
- returns the snapshot at that index.

This is the fastest lookup path and is used by most navigation operations.

### 2. Timestamp reference
If `ref` is a datetime:
- validates the type,
- scans the history for a matching timestamp,
- returns the associated snapshot.

If no timestamp matches, a structured validation error is raised.

### 3. Invalid reference type
If `ref` is neither an integer nor a datetime, the function raises a dedicated
validation error describing the expected types.

## Integration requirements
The function assumes the instance implements:

- **History internals**  
  `_history`, `_history_count`, `_history_index`

- **SnapshotMixin**  
  Snapshot tuples are produced by `_build_snapshot()` and stored in history.

Without these components, the lookup mechanism cannot operate correctly.

## Why this function exists
History navigation must support two reference modes:

- **index-based** (fast, positional, stable)
- **timestamp-based** (semantic, human-readable)

Supporting both makes the history subsystem flexible and intuitive while
remaining deterministic.

## Deterministic behavior
Snapshot lookup is guaranteed to be:

- stable,
- predictable,
- type-safe,
- consistent across all history operations.

This determinism is essential for undo/redo, diffing, debugging, and
serialization.

## Stability guarantee
Any change to this function would affect:

- navigation correctness,
- diffing behavior,
- history import/export,
- undo/redo logic,
- debugging tools.

Therefore, `find_snapshot` is treated as a **core invariant** of the history
subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by mixins.
- All structural logic is delegated to history internals.
"""