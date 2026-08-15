from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .validations import raise_stepper_down_limit_reached
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.numerical.stepper import StepperProtocol


def verify_down_limit(
    self: "StepperProtocol",
    new_value: Any,
    *,
    raise_exception: bool = False
) -> bool:
    """
    Verifies that the new value does not fall below the stepper's down limit.

    If the down limit is set and the new value is below it,
    triggers the optional limit action and optionally raises a structured error.
    """

    # 1. Check whether the DOWN limit is set and violated
    if self.down_limit is not UNSET and new_value < self.down_limit:

        # 2. Trigger limit action if present
        if self.down_limit_action:
            self.down_limit_action()

        # 3. Raise structured error if requested
        if raise_exception:
            raise_stepper_down_limit_reached(self, new_value)

        return False

    # 4. Successful validation
    return True


_DESIGN_NOTES = """
# verify_down_limit

## Purpose
Checks whether a new value violates the configured down limit of the stepper.
If the limit is violated, the function:

1. triggers the optional `down_limit_action`,
2. optionally raises a structured diagnostic error,
3. returns `False` to indicate validation failure.

This function provides the core logic for lower-bound enforcement in stepper
operations.

---

## Architectural role
`verify_down_limit` is used by:

- `step_down`
- `step_up`
- `set_value`

It acts as the canonical validation layer for lower-bound limit checks.

The function integrates with:

- structured error raising (`raise_stepper_down_limit_reached`),
- optional callback execution (`down_limit_action`),
- UNSET semantics for optional configuration.

---

## How it works

### 1. Limit presence and violation check
The function first checks:

```
self.down_limit is not UNSET
and new_value < self.down_limit
```

This ensures that:

- limits are only enforced when explicitly configured,
- numeric comparison is performed only when meaningful.

### 2. Triggering limit actions
If a violation occurs and a `down_limit_action` is configured, it is executed
immediately.  
This allows users to attach custom behavior such as logging, clamping, or
side-effect operations.

### 3. Structured error raising
If `raise_exception=True`, the function raises a structured diagnostic error
via `raise_stepper_down_limit_reached`.

This replaces generic exceptions with rich, contextual, and actionable error
messages consistent with the Simple ecosystem.

### 4. Returning validation status
If no exception is raised, the function returns `False` to indicate that the
limit was violated.

If the limit is not violated, the function returns `True`.

---

## Why this function exists
Stepper operations must enforce numeric boundaries to prevent invalid state
transitions.  
This function encapsulates:

- limit checking,
- callback execution,
- structured error raising,
- UNSET semantics,
- consistent return values.

It ensures predictable behavior across all stepper operations.

---

## Deterministic behavior
The function guarantees:

- stable limit checking,
- consistent callback execution,
- predictable error raising,
- deterministic return values.

This determinism is essential for safe numeric stepping.

---

## Notes
- This function is internal and not part of the public API.
- All structural logic is delegated to limit configuration and validation utilities.
- The function is intentionally minimal and side-effect-free except for
  optional callback execution.
"""