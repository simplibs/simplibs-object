from .CollectionBase import CollectionBase
from .Iterable import Iterable
from .Mapping import Mapping
from .main import Collection


_DESIGN_NOTES = """
# Collections Dunders

## Purpose
Gives composite instances dict-like and iterable behavior over their
direct inners — iteration, `len()`, item access, and the combined
`Collection` bundle.

## Components

| Component           | Type  | Description                                                      |
| :------------------ | :---- | :--------------------------------------------------------------- |
| `CollectionBase`    | Mixin | Base mapping foundation — `keys()`, `values()`, `items()`.       |
| `Iterable`          | Mixin | `__iter__`, `__reversed__`, `__dir__` over inner keys.           |
| `Mapping`           | Mixin | `__getitem__`, `__setitem__`, `__contains__`, `__len__`, `get()`.|
| `Collection`        | Mixin | Combines `Iterable` + `Mapping` (see `.main`).                   |

## Notes
- All components are `_composite_only` — atoms have no inners to
  collect over.
- `Iterable` and `Mapping` share their frozen key set via `CollectionBase`,
  computed once in `init_mixins`.
"""
