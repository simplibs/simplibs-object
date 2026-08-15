from .Stepper import Stepper


_DESIGN_NOTES = """
# Stepper Class

## Purpose
Provides the core Stepper class used by numerical mixins to safely manipulate
numeric values with full support for:

- type normalization,
- semantic validation,
- upper and lower limit enforcement,
- limit actions,
- controlled stepping operations.

The Stepper acts as a dedicated controller for numeric transitions and forms
the backbone of the numerical subsystem (`Volume`, `Equalizer`).

## Components

| Component | Type    | Description                                      |
| :-------- | :-------| :----------------------------------------------- |
| `Stepper` | Class   | Implements the full stepping, validation, and limit logic. |

## Notes
- This class is internal and not part of the public API.
- All operational logic is delegated to processor and validation submodules.
- The Stepper guarantees deterministic, safe numeric transitions.
- It is instantiated automatically by numerical mixins and never directly by the user.
"""
