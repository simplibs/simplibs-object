from .ClassGetItem import ClassGetItem


_DESIGN_NOTES = """
# Generics Dunders

## Purpose
Gives Simple classes generic-style subscript syntax (`MyClass[int]`) for
typing/IDE purposes, without requiring inheritance from `typing.Generic`.

## Components

| Component          | Type  | Description                                             |
| :----------------- | :---- | :------------------------------------------------------ |
| `ClassGetItem`     | Mixin | `__class_getitem__` fallback for subscriptable classes. |

## Notes
- Purely syntactic — has no effect on instance construction or runtime
  behavior.
"""
