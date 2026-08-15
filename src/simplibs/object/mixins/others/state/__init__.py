from .DefaultState import DefaultState
from .DirtyTracking import DirtyTracking
from .History import History
from .Permission import Permission


_DESIGN_NOTES = """
# State Mixins

## Purpose
State-management mixins for mutable instances — remembering an initial
state, tracking unsaved changes, recording a full undo/redo history, and
runtime read-only locking.

## Components

| Component          | Type  | Description                                                            |
| :----------------- | :---- | :--------------------------------------------------------------------- |
| `DefaultState`     | Mixin | Remembers construction-time state; reset/clone/new-default.            |
| `DirtyTracking`    | Mixin | `is_dirty`, `dirty_paths`, `mark_clean()`, `reset_to_clean()`.         |
| `History`          | Mixin | Full undo/redo history — record, navigate, diff, export/import.        |
| `Permission`       | Mixin | Runtime `lock()` / `unlock()` read-only toggle.                        |

## Notes
- All four are `_mutable_only` — every one of them concerns in-place
  state that has no meaning on an immutable instance.
- `Permission`'s `_locked` attribute and its enforcement are not set up
  by this mixin — they are built directly into every atomic instance via
  `create_atom_init` and `create_value_setter`; `Permission` only exposes
  a friendly API over that existing infrastructure.
"""
