from .Arithmetic import Arithmetic
from .Bitwise import Bitwise
from .Conversion import Conversion
from .Inplace import Inplace
from .Unary import Unary


_DESIGN_NOTES = """
# Numeric Dunders

## Purpose
Gives Simple instances the full range of Python numeric protocols —
binary and unary arithmetic, bitwise operations, in-place arithmetic, and
conversion to native Python numeric types.

## Components

| Component          | Type  | Description                                                               |
| :----------------- | :---- | :------------------------------------------------------------------------ |
| `Arithmetic`       | Mixin | `+ - * / // % **` and reflected forms, returns new instances.             |
| `Unary`            | Mixin | `-x`, `+x`, `abs(x)`, returns new instances.                              |
| `Bitwise`          | Mixin | `& \\| ^ << >> ~` for integral atoms only.                                |
| `Inplace`          | Mixin | `+= -= *= /= //= %= **=`, mutates in place, `_mutable_only`.              |
| `Conversion`       | Mixin | `int()`, `float()`, `complex()`, `round()`, `__index__`, floor/ceil/trunc.|

## Notes
- `Arithmetic`, `Unary`, `Conversion` restrict to `_only_types = Number`.
- `Bitwise` further restricts to `_constant_only` + `_only_types = Integral`.
- `Inplace` is `_mutable_only`; every other mixin here returns a new
  instance rather than mutating `self`.
"""
