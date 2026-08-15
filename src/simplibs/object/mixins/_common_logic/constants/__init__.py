from .names import HISTORY, OWNER_CLASS, STEPPER, VALUE
from .sets import FORBIDDEN_NAMES, RESTRICTION_FLAGS

_DESIGN_NOTES = """
# Simple Mixin Constants Package

## Purpose
Aggregates all internal constants used by the Simple mixin subsystem. Provides
a unified import surface for attribute name tokens and structural constraint
sets.

## Internal Components Registry

| Component           | Type     | Description                                              |
| :------------------ | :------- | :------------------------------------------------------- |
| `HISTORY`           | Constant | Canonical internal attribute name for history tracking. |
| `OWNER_CLASS`       | Constant | Canonical internal attribute name for owner class.      |
| `STEPPER`           | Constant | Canonical internal attribute name for stepper logic.    |
| `VALUE`             | Constant | Canonical internal attribute name for value storage.    |
| `FORBIDDEN_NAMES`   | Set      | Reserved internal names that mixins must never define.   |
| `RESTRICTION_FLAGS` | Tuple    | Declarative mixin compatibility flag identifiers.        |

## Notes
This package acts as the single authoritative source of truth for all mixin
constants. Its stability is essential for correct runtime behavior across the
entire Simple object system.
"""
