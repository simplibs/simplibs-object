from .HistoryDict import HistoryDict
from .HistoryEntry import HistoryEntry

_DESIGN_NOTES = """
# History Alias Typings Sub-Package

## Purpose
Provides type definitions for history timeline tracking, state snapshots over time, and export containers.

## Internal Components Registry

| Component      | Type      | Description                                                                  |
| :------------- | :-------- | :--------------------------------------------------------------------------- |
| `HistoryDict`  | TypeAlias | Serialized dictionary format holding the exported history data package.      |
| `HistoryEntry` | TypeAlias | Timestamped tuple entry `(datetime, SnapshotTuple)` recording a state point. |
"""