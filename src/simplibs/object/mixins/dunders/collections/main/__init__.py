from .Collection import Collection


_DESIGN_NOTES = """
# Collection Main

## Purpose
Bundles the individual collection-related dunder mixins into one
ready-to-use combined mixin.

## Components

| Component     | Type  | Description                                              |
| :------------ | :---- | :------------------------------------------------------- |
| `Collection`  | Mixin | Combines `Iterable` + `Mapping` into full dict-like API. |

## Notes
- Use `Collection` when a composite needs the complete iteration + item
  access surface; use `Iterable` or `Mapping` alone for a partial subset.
"""
