from .Copyable import Copyable
from .PickleState import PickleState
from .PickleReduce import PicleReduce
from .main import Lifecycle


_DESIGN_NOTES = """
# Lifecycles Dunders

## Purpose
Gives Simple instances standard Python object-lifecycle protocols —
`copy`/`deepcopy` support and full `pickle` support — both built on the
same underlying snapshot/serialization foundation.

## Components

| Component          | Type  | Description                                                            |
| :----------------- | :---- | :--------------------------------------------------------------------- |
| `Copyable`         | Mixin | `__copy__` / `__deepcopy__` via snapshot.                              |
| `PickleState`      | Mixin | `__getstate__` / `__setstate__` via `to_dict()` / `from_dict()`.       |
| `PicleReduce`      | Mixin | `__reduce__` — top-level pickle protocol hook, built on `PickleState`. |
| `Lifecycle`        | Mixin | Combines `Copyable` + `PicleReduce` (see `.main`).                     |

## Notes
- `PicleReduce` keeps its original spelling (missing a "k") to match the
  existing codebase — not a translation artifact.
- Dependency order: `PickleState` → `PicleReduce`; `Copyable` and
  `PicleReduce` are combined into `Lifecycle`.
"""
