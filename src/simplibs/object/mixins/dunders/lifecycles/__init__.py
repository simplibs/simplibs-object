from .Copyable import Copyable
from .PickleState import PickleState
from .PickleReduce import PickleReduce
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
| `PickleReduce`      | Mixin | `__reduce__` — top-level pickle protocol hook, built on `PickleState`. |
| `Lifecycle`        | Mixin | Combines `Copyable` + `PickleReduce` (see `.main`).                     |

## Notes
- `PickleReduce` keeps its original spelling (missing a "k") to match the
  existing codebase — not a translation artifact.
- Dependency order: `PickleState` → `PickleReduce`; `Copyable` and
  `PickleReduce` are combined into `Lifecycle`.
"""
