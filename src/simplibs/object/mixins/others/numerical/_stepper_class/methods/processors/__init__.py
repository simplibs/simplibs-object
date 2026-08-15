from .process_step_value import process_step_value
from .verify_down_limit import verify_down_limit
from .verify_up_limit import verify_up_limit


_DESIGN_NOTES = """
# Stepper Runtime Processors

## Purpose
Provides the core runtime helper functions used by the Stepper's stepping
operations. These processors implement the essential mechanics of:

- step value normalization,
- upward and downward limit enforcement,
- structured error raising and optional limit actions.

They form the operational backbone of the stepper subsystem and are used by
all stepping methods (`step_up`, `step_down`, `set_value`).

## Components

| Component            | Type     | Description                                                       |
| :------------------- | :--------| :---------------------------------------------------------------- |
| `process_step_value` | Function | Normalizes and validates the step value used for stepping.        |
| `verify_down_limit`  | Function | Checks lower limit violations and triggers optional actions.       |
| `verify_up_limit`    | Function | Checks upper limit violations and triggers optional actions.       |

## Notes
- These utilities are internal and not part of the public API.
- They are used exclusively by the stepper's stepping and value‑assignment methods.
- All structural logic is delegated to the stepper's validation subsystem.
- Errors raised here follow the SimpleLogicError diagnostic format.
"""
