from .ImmutableMethods import ImmutableMethods
from .ImmutableMethodsWithInners import ImmutableWithInners


_DESIGN_NOTES = """
# Immutable Mixins

## Purpose
The "change without mutating" API for immutable instances — both the
generic core methods and the per-inner generated setters.

## Components

| Component                  | Type  | Description                                                     |
| :------------------------- | :---- | :-------------------------------------------------------------- |
| `ImmutableMethods`         | Mixin | `with_constant`, `with_composite`, `with_changes`, `duplicate`. |
| `ImmutableWithInners`      | Mixin | Generates a dedicated `with_<name>(value)` per inner.           |

## Notes
- Both are `_immutable_only`; `ImmutableWithInners` is additionally
  `_composite_only`, since it has nothing to generate for atoms.
- `ImmutableWithInners` extends `ImmutableMethods` and reuses
  `with_composite` internally for every generated setter.
"""
