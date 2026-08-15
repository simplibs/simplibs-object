from .Lifecycle import Lifecycle


_DESIGN_NOTES = """
# Lifecycle Main

## Purpose
Bundles the individual lifecycle-related dunder mixins into one
ready-to-use combined mixin.

## Components

| Component     | Type  | Description                                                  |
| :------------ | :---- | :----------------------------------------------------------- |
| `Lifecycle`   | Mixin | Combines `Copyable` + `PicleReduce` for copy/pickle support. |

## Notes
- Use `Lifecycle` when an instance needs both `copy`/`deepcopy` and
  `pickle` support; use the individual mixins for just one protocol.
"""
