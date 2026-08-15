from .Equalizer import Equalizer
from .Volume import Volume


_DESIGN_NOTES = """
# Numerical Mixins

## Purpose
Attaches `Stepper` controllers — safe, bounded numeric stepping — to
instance values, either the single value of an atom or every inner of a
composite.

## Components

| Component      | Type  | Description                                                 |
| :------------- | :---- | :---------------------------------------------------------- |
| `Volume`       | Mixin | One stepper for the instance's own main value.              |
| `Equalizer`    | Mixin | One stepper per inner, exposed as dynamic properties.       |

## Notes
- Both are `_mutable_only` and `_only_types = Number`.
- `Volume` targets atoms (single value); `Equalizer` targets composites
  (`_composite_only`), generating one property per inner via
  `__extend_instance_class__`.
"""
