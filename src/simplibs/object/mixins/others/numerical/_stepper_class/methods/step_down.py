from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .processors import process_step_value, verify_down_limit
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.numerical.stepper import StepperProtocol
    from ......_core.protocols.mixins.numerical.stepper.internal_types import StepValue


def step_down(
    self: "StepperProtocol",
    value: "StepValue" = UNSET,
    *,
    validate: bool = True,
    raise_exception: bool = False
) -> Any:
    """
    Decreases the instance’s value by the defined step (or a provided value).
    Enforces configured limits and triggers optional actions.
    """

    # 1. Normalize and validate the step value
    _value = process_step_value(self, value, validate=validate)

    # 2. Compute the new value
    # noinspection PyProtectedMember
    new_value = self._instance._value - _value

    # 3. Check lower limit
    if not verify_down_limit(self, new_value, raise_exception=raise_exception):
        return False

    # 4. Write the new value
    self._instance._value = new_value
    return True


_DESIGN_NOTES = """
# step_down

## Purpose
Decreases the instance’s value by a defined step or a user-provided value.
This method enforces:

- numeric normalization,
- instance-level validation,
- lower limit checks,
- optional structured error raising,
- optional limit actions.

It provides the canonical logic for downward stepping in the Stepper subsystem.

---

## Architectural role
`step_down` is one of the two primary stepping operations:

- `step_up` increases the value,
- `step_down` decreases the value.

It integrates with:

- `process_step_value` for normalization and validation,
- `verify_down_limit` for lower-bound enforcement,
- structured error raising via limit validation functions,
- UNSET semantics for optional step configuration.

---

## How it works

### 1. Step value normalization
The function first calls:

```
_value = process_step_value(self, value, validate=validate)
```

This ensures:

- type consistency with the instance’s numeric type,
- optional semantic validation,
- safe conversion of user-provided step values.

### 2. Compute the new value
The new value is computed as:

```
new_value = current_value - step_value
```

This is the only arithmetic operation in the method.

### 3. Lower limit enforcement
The function calls:

```
verify_down_limit(self, new_value, raise_exception)
```

This enforces:

- lower numeric boundaries,
- optional limit actions,
- optional structured error raising.

If the limit is violated and no exception is raised, the method returns `False`.

### 4. Write the new value
If all checks pass, the new value is written:

```
self._instance._value = new_value
```

This is the only place where the method mutates the instance’s value.

---

## Why this function exists
Stepper must guarantee safe and predictable downward transitions.  
This function encapsulates:

- normalization,
- validation,
- limit enforcement,
- structured error raising,
- deterministic assignment.

It ensures that invalid or unsafe transitions never reach deeper layers of the
Stepper pipeline.

---

## Deterministic behavior
The function guarantees:

- stable normalization,
- predictable limit checking,
- consistent error raising,
- deterministic return values,
- safe mutation of the instance.

This determinism is essential for safe numeric stepping.

---

## Notes
- This function is internal and not part of the public API.
- All structural logic is delegated to processors and validation utilities.
- The function is intentionally minimal and side-effect-free except for the
  final value assignment.
"""