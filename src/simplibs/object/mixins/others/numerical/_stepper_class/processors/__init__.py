from .process_down_limit_value import process_down_limit_value
from .process_limit_action import process_limit_action
from .process_up_limit_value import process_up_limit_value
from .process_value import process_value
from .validate_instance import validate_instance


_DESIGN_NOTES = """
# Stepper Configuration Processors

## Purpose
Provides the core configuration processors used by the Stepper subsystem.
These processors implement the essential mechanics of:

- value normalization,
- limit preparation and consistency validation,
- callable action validation,
- instance protocol and numeric validation.

They form the configuration backbone of the stepper subsystem and ensure that
all values, limits, and actions are valid before entering the runtime pipeline.

## Components

| Component                   | Type     | Description                                                         |
| :-------------------------- | :--------| :------------------------------------------------------------------ |
| `process_value`             | Function | Normalizes and optionally validates values for stepping operations. |
| `process_down_limit_value`  | Function | Prepares and validates the down-limit value.                        |
| `process_up_limit_value`    | Function | Prepares and validates the up-limit value.                          |
| `process_limit_action`      | Function | Validates that limit actions are callable.                          |
| `validate_instance`         | Function | Ensures the instance satisfies protocol and numeric requirements.   |

## Notes
- These utilities are internal and not part of the public API.
- They are used exclusively during Stepper initialization and configuration.
- All structural logic is delegated to validation helpers and instance-level rules.
- Errors raised here follow the SimpleRuntimeError diagnostic format.
"""
