from .FORBIDDEN_NAMES import FORBIDDEN_NAMES
from .RESTRICTION_FLAGS import RESTRICTION_FLAGS

_DESIGN_NOTES = """
# Mixin Structural Constraint Sets

## Purpose
Provides centralized sets of structural constraints used by the mixin
validation pipeline. These sets define forbidden attribute names and allowed
declarative compatibility flags.

## Internal Components Registry

| Component           | Type     | Description                                              |
| :------------------ | :------- | :------------------------------------------------------- |
| `FORBIDDEN_NAMES`   | Set      | Reserved internal names that mixins must never define.   |
| `RESTRICTION_FLAGS` | Tuple    | Declarative mixin compatibility flag identifiers.        |

## Notes
These sets act as schema definitions for mixin structure. They are intentionally
small, explicit, and immutable to ensure deterministic validation behavior.
"""
