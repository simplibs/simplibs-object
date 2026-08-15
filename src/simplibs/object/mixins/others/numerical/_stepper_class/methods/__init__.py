from .set_value import set_value
from .step_down import step_down
from .step_up import step_up


_DESIGN_NOTES = """
# Stepper Core Methods

## Purpose
Provides the primary operational methods of the Stepper subsystem. These
methods implement the controlled mutation of the instance's numeric value,
including:

- direct value assignment,
- upward stepping,
- downward stepping,
- full enforcement of numeric limits and optional limit actions.

They form the public-facing API of the Stepper and are used by all numerical
mixins (`Volume`, `Equalizer`) and any user-level stepping operations.

## Components

| Component     | Type     | Description                                                        |
| :------------ | :--------| :----------------------------------------------------------------- |
| `set_value`   | Function | Safely assigns a new value with full limit validation.             |
| `step_down`   | Function | Decreases the value by a defined step and enforces down limits.    |
| `step_up`     | Function | Increases the value by a defined step and enforces up limits.      |

## Notes
- These methods form the core public API of the Stepper.
- All structural logic is delegated to processor utilities and validation helpers.
- Limit actions and structured errors follow the SimpleLogicError diagnostic format.
- These methods guarantee deterministic, safe numeric transitions.
"""
