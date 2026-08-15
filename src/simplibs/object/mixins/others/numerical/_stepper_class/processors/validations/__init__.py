from .raise_stepper_invalid_action import raise_stepper_invalid_action
from .raise_stepper_invalid_down_limit import raise_stepper_invalid_down_limit
from .raise_stepper_invalid_instance import raise_stepper_invalid_instance
from .raise_stepper_invalid_up_limit import raise_stepper_invalid_up_limit
from .raise_stepper_non_numeric_value import raise_stepper_non_numeric_value


_DESIGN_NOTES = """
# Stepper Configuration Validations

## Purpose
Provides the validation functions responsible for verifying the correctness
of all configuration values used by the Stepper subsystem. These validators
ensure that:

- limit values are consistent,
- limit actions are callable,
- instances satisfy the required protocol,
- numeric values are valid and safe for stepping.

They form the configuration safety layer of the Stepper and prevent invalid
states from entering the runtime pipeline.

## Components

| Component                         | Type     | Description                                                        |
| :-------------------------------- | :--------| :----------------------------------------------------------------- |
| `raise_stepper_invalid_action`    | Function | Raised when a limit action is not callable.                        |
| `raise_stepper_invalid_down_limit`| Function | Raised when the down limit is higher than the up limit.            |
| `raise_stepper_invalid_instance`  | Function | Raised when the provided instance does not satisfy the protocol.   |
| `raise_stepper_invalid_up_limit`  | Function | Raised when the up limit is lower than the down limit.             |
| `raise_stepper_non_numeric_value` | Function | Raised when the instance value is not numeric.                     |

## Notes
- These utilities are internal and not part of the public API.
- They are used exclusively by configuration processors (`process_value`, `process_limit_action`, etc.).
- All errors follow the SimpleLogicError diagnostic format.
- Validators here protect the Stepper from invalid configuration before runtime.
"""
