from typing import Any, TYPE_CHECKING
# Inners
from .validations import raise_stepper_invalid_action
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.numerical.stepper import StepperProtocol
    from ....._core.protocols.mixins.numerical.stepper.internal_types import LimitAction


def process_limit_action(
    self: "StepperProtocol",
    value: Any
) -> "LimitAction":
    """
    Validates and returns the limit action for the stepper.

    Ensures that the provided value is a callable object that can be executed
    when the upper or lower limit is reached.
    """

    # 1. Validate callable
    if not callable(value):
        raise_stepper_invalid_action(self, value)

    # 2. Return the validated action
    return value


_DESIGN_NOTES = """
# process_limit_action

## Purpose
Validates and prepares the limit action used by the stepper.  
This function ensures that any action assigned to:

- `up_limit_action`
- `down_limit_action`

is a valid callable object that can be executed when a limit is reached.

It provides the canonical logic for configuring limit callbacks.

---

## Architectural role
`process_limit_action` is used by the setters:

```
Stepper.up_limit_action = ...
Stepper.down_limit_action = ...
```

It acts as the validation layer for callback configuration.

The function integrates with:

- `raise_stepper_invalid_action` for structured error reporting,
- Stepper’s limit‑checking functions (`verify_up_limit`, `verify_down_limit`),
- UNSET semantics for optional callback configuration.

---

## How it works

### 1. Callable validation
The function checks:

```
callable(value)
```

If false, the configuration is invalid because limit actions must be executable
callbacks.  
Violations are reported using a structured diagnostic error.

### 2. Returning the validated action
If validation succeeds, the callable object is returned unchanged and stored
as the new limit action.

---

## Why this function exists
Stepper supports optional callbacks that are executed when numeric boundaries
are crossed.  
These callbacks must be:

- callable,
- side‑effect‑safe,
- predictable,
- consistent with the instance’s behavior.

This function encapsulates:

- validation,
- structured error raising,
- deterministic return behavior.

It ensures that invalid callbacks never reach deeper layers of the stepper
pipeline.

---

## Deterministic behavior
The function guarantees:

- stable validation,
- predictable error raising,
- deterministic return values.

This determinism is essential for safe numeric stepping.

---

## Notes
- This function is internal and not part of the public API.
- All structural logic is delegated to validation utilities.
- The function is intentionally minimal and side‑effect‑free.
"""