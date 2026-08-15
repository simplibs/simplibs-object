from .DefaultStateProtocol import DefaultStateProtocol
from .DirtyTrackingProtocol import DirtyTrackingProtocol
from .PermissionProtocol import PermissionProtocol
from .HistoryProtocol import HistoryProtocol


_DESIGN_NOTES = """
# State Mixin Protocols Sub-Package

## Purpose
Defines protocols for state lifecycle management, change tracking, timeline cascades (Undo/Redo),
and write-access locking.

## Internal Components Registry

| Component               | Type     | Description                                                                  |
| :---------------------- | :------- | :--------------------------------------------------------------------------- |
| `DefaultStateProtocol`  | Protocol | Manages initial baseline state, cloning, and instance resets.                |
| `DirtyTrackingProtocol` | Protocol | Tracks modified paths against clean state baselines and handles rollbacks.   |
| `HistoryProtocol`       | Protocol | Full timeline management with Undo/Redo cascades, timestamps, and diffs.     |
| `PermissionProtocol`    | Protocol | Read-only mode locking and write-access authorization controls.              |
"""