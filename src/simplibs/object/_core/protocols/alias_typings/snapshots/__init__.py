from .SnapshotDict import SnapshotDict
from .SnapshotDiffItem import SnapshotDiffItem
from .SnapshotDiffTuple import SnapshotDiffTuple
from .SnapshotTuple import SnapshotTuple

_DESIGN_NOTES = """
# Snapshots Alias Typings Sub-Package

## Purpose
Provides type definitions for immutable state snapshots, state differences, and diff tuples.

## Internal Components Registry

| Component           | Type      | Description                                                                  |
| :------------------ | :-------- | :--------------------------------------------------------------------------- |
| `SnapshotDict`      | TypeAlias | Key-value dictionary snapshot holding named element states.                  |
| `SnapshotDiffItem`  | TypeAlias | Triplet `(element_path, old_value, new_value)` recording a single state diff.|
| `SnapshotDiffTuple` | TypeAlias | Tuple holding multiple state difference items for change tracking.          |
| `SnapshotTuple`     | TypeAlias | Immutable sequence tuple capturing raw values across composite elements.     |
"""