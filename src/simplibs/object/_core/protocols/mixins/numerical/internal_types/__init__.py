from .SteppersMap import SteppersMap

_DESIGN_NOTES = """
# Numerical Internal Types Sub-Package

## Purpose
Provides internal type aliases used by numerical mixins for stepper mapping and lookup.

## Internal Components Registry

| Component      | Type      | Description                                                                  |
| :------------- | :-------- | :--------------------------------------------------------------------------- |
| `SteppersMap`  | TypeAlias | Key-value mapping of snake_case node names to their respective Steppers.     |
"""