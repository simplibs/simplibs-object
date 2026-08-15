from .ValueDisplay import ValueDisplay
from .ValueFormatting import ValueFormatting


_DESIGN_NOTES = """
# Representation Dunders

## Purpose
Controls how a Simple instance presents itself as text and how its
value converts to formatted strings, bytes, and booleans.

## Components

| Component            | Type  | Description                                                       |
| :------------------- | :---- | :---------------------------------------------------------------- |
| `ValueDisplay`       | Mixin | `__repr__` / `__str__` — value-like display, `_constant_only`.    |
| `ValueFormatting`    | Mixin | `format()` / `__format__` / `__bytes__` / `__bool__`.             |

## Notes
- `ValueDisplay` is opt-in and constant-only by design — most instances
  should keep the default structural `__repr__`/`__str__`.
- `ValueFormatting` works for both atoms and composites and does not
  touch `__repr__`/`__str__`, so the two mixins can be combined freely.
"""
