from .Equality import Equality
from .Ordering import Ordering


_DESIGN_NOTES = """
# Comparison Dunders

## Purpose
Gives Simple instances value-based equality, hashing, and magnitude
ordering — the two independent comparison protocols Python distinguishes
between.

## Components

| Component   | Type  | Description                                                  |
| :---------- | :---- | :----------------------------------------------------------- |
| `Equality`  | Mixin | `__eq__` and `__hash__`, mutability-aware hashing strategy.  |
| `Ordering`  | Mixin | `__lt__`, `__le__`, `__gt__`, `__ge__` via `self.value`.     |

## Notes
- The two mixins are independent — a class may combine both, or use only
  one, depending on whether ordering makes sense for its value type.
- `Equality`'s hashing strategy branches on `__is_mutable__`: identity
  hash for mutable instances, value hash for immutable ones.
"""
