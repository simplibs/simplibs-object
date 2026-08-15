from typing import Any, TYPE_CHECKING
# Outers
from ..processors import process_value
# Inners
from .processors import verify_up_limit, verify_down_limit
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.numerical.stepper import StepperProtocol


def set_value(
    self: "StepperProtocol",
    value: Any,
    *,
    validate: bool = True,
    raise_exception: bool = False
) -> Any:
    """
    Safely writes a new value into the instance with full limit and action control.
    """

    # 1. Normalize and validate the value
    _value = process_value(self, value, validate=validate)

    # 2. Handle identical value (no-op)
    # noinspection PyProtectedMember
    if _value == self._instance._value:
        return True

    # 3. Limit checks
    # noinspection PyProtectedMember
    if _value > self._instance._value:
        if not verify_up_limit(self, _value, raise_exception=raise_exception):
            return False
    else:
        if not verify_down_limit(self, _value, raise_exception=raise_exception):
            return False

    # 4. Write the value
    self._instance._value = _value
    return True


_DESIGN_NOTES = """
# set_value

## Purpose
Safely writes a new value into the instance while enforcing:

- numeric normalization,
- instance-level validation,
- upper and lower limit checks,
- optional structured error raising,
- optional limit actions.

This function is the central entry point for controlled value assignment in the
Stepper subsystem.

---

## Architectural role
`set_value` is used whenever the stepper needs to assign a new value:

- direct user assignment (`stepper.set_value(x)`),
- internal stepping (`step_up`, `step_down`),
- composite or pipeline-driven updates.

It integrates with:

- `process_value` for normalization and validation,
- `verify_up_limit` and `verify_down_limit` for boundary enforcement,
- structured error raising via limit validation functions,
- UNSET semantics for optional limit configuration.

---

## How it works

### 1. Value normalization and validation
The function first calls:

```
_value = process_value(self, value, validate=validate)
```

This ensures:

- type consistency with the instance’s numeric type,
- optional semantic validation,
- safe conversion of user-provided values.

### 2. No-op optimization
If the new value equals the current instance value, the function returns `True`
immediately.  
This avoids unnecessary limit checks and assignments.

### 3. Limit enforcement
The function determines whether the new value is:

- **higher** than the current value → check upper limit,
- **lower** than the current value → check lower limit.

It calls:

```
verify_up_limit(self, _value, raise_exception)
verify_down_limit(self, _value, raise_exception)
```

These functions:

- enforce numeric boundaries,
- trigger limit actions,
- optionally raise structured errors,
- return `False` when the limit is violated.

If a limit is violated and no exception is raised, `set_value` returns `False`.

### 4. Writing the value
If all checks pass, the function writes the new value:

```
self._instance._value = _value
```

This is the only place where the stepper directly mutates the instance’s value.

---

## Why this function exists
Stepper must guarantee safe and predictable value transitions.  
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