from .raise_stepper_down_limit_reached import raise_stepper_down_limit_reached
from .raise_stepper_up_limit_reached import raise_stepper_up_limit_reached


_DESIGN_NOTES = """
# Stepper Limit-Reached Validations

## Purpose
Provides the specialized validation functions used when a stepper value
crosses its configured numeric boundaries. These functions raise structured,
diagnostic errors that describe the limit violation in detail and offer
actionable guidance.

They form the core of the stepper's runtime safety layer, ensuring that
invalid transitions are detected early and handled consistently.

## Components

| Component                         | Type     | Description                                               |
| :-------------------------------- | :--------| :-------------------------------------------------------- |
| `raise_stepper_down_limit_reached`| Function | Raises an error when the new value falls below the down limit. |
| `raise_stepper_up_limit_reached`  | Function | Raises an error when the new value exceeds the up limit.       |

## Notes
- These utilities are internal and not part of the public API.
- They are used exclusively by `verify_down_limit` and `verify_up_limit`.
- All structural logic is delegated to the stepper's validation subsystem.
- Errors raised here follow the SimpleRuntimeError diagnostic format.
"""
