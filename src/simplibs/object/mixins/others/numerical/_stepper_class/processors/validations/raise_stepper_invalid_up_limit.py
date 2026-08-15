from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.numerical.stepper import StepperProtocol


def raise_stepper_invalid_up_limit(
    stepper: "StepperProtocol",
    up_limit_value: Any,
) -> NoReturn:
    """
    Raises a structured error when the provided upper limit is lower
    than the currently configured down limit.
    """

    raise SimpleLogicError(
        error_name="STEPPER LIMIT CONFIGURATION ERROR",
        label="up limit",
        value=up_limit_value,
        expected=f"Value >= {stepper.down_limit!r}",
        problem=(
            "The provided upper limit is lower than the configured down limit. "
            "This creates an invalid numeric boundary configuration."
        ),
        context=(
            f"Instance type: {type(stepper._instance).__name__}.",
            f"Current value: {stepper._instance.value!r}.",
            f"Down limit: {stepper.down_limit!r}.",
            f"Attempted up limit: {up_limit_value!r}.",
            "The stepper requires consistent numeric boundaries where "
            "down_limit <= up_limit."
        ),
        how_to_fix=(
            "Set the upper limit to a value greater than or equal to the down limit.",
            "If you need to restrict the allowed range, lower the down limit first.",
            "Ensure that both limits reflect a valid numeric interval.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_stepper_invalid_up_limit

## Purpose
Provides a structured diagnostic error when a user attempts to configure
an upper limit that is lower than the currently configured down limit.  
This replaces the generic `ValueError("Up limit nemůže být menší než down limit")`
with a rich, contextual, and actionable error message consistent with the
Simple ecosystem.

This protects the stepper from invalid numeric boundary configurations.

---

## Architectural reasoning
Stepper enforces numeric boundaries:

- `down_limit` defines the minimum allowed value,
- `up_limit` defines the maximum allowed value.

These boundaries must satisfy:

```
down_limit <= up_limit
```

If this condition is violated:

- step operations become undefined,
- limit checks break,
- callbacks may fire incorrectly,
- the instance can enter an invalid state.

Therefore, the error must:

- clearly explain the violation,
- show both limits,
- show the attempted value,
- provide actionable steps,
- include contextual information about the instance.

This mirrors the design of immutability, history, metadata, and composite errors.

---

## Pipeline position
This function is used inside `process_up_limit_value`:

1. Normalize the provided value.
2. Check if `up_limit < down_limit`.
3. If yes → call this function.
4. Otherwise return the normalized value.

This ensures:

- consistent validation,
- predictable error handling,
- clear separation of validation and error raising.

---

## Diagnostic value
The error message includes:

- the invalid upper limit value,
- the expected minimum (down limit),
- the current instance value,
- the configured down limit,
- the instance type,
- actionable steps to resolve the issue.

This makes debugging significantly easier and aligns with the philosophy of
Simple’s structured error system.

---

## Notes
- This is a pure `raise_...` function: it performs no branching logic.
- It is internal and not part of the public API.
- All limit configuration errors must use this function.
- The error type is `SimpleLogicError` with `ValueError` as the underlying exception.
"""