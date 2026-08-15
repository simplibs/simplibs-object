from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.numerical.stepper import StepperProtocol


def raise_stepper_invalid_down_limit(
    stepper: "StepperProtocol",
    down_limit_value: Any,
) -> NoReturn:
    """
    Raises a structured error when the provided down limit is higher
    than the currently configured up limit.
    """

    raise SimpleLogicError(
        error_name="STEPPER LIMIT CONFIGURATION ERROR",
        label="down limit",
        value=down_limit_value,
        expected=f"Value <= {stepper.up_limit!r}",
        problem=(
            "The provided down limit is higher than the configured up limit. "
            "This creates an invalid numeric boundary configuration."
        ),
        context=(
            f"Instance type: {type(stepper._instance).__name__}.",
            f"Current value: {stepper._instance.value!r}.",
            f"Up limit: {stepper.up_limit!r}.",
            f"Attempted down limit: {down_limit_value!r}.",
            "The stepper requires consistent numeric boundaries where "
            "down_limit <= up_limit."
        ),
        how_to_fix=(
            "Set the down limit to a value lower than or equal to the up limit.",
            "If you need to expand the allowed range, increase the up limit first.",
            "Ensure that both limits reflect a valid numeric interval.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_stepper_invalid_down_limit

## Purpose
Provides a structured diagnostic error when a user attempts to configure
a down limit that is higher than the currently configured up limit.  
This replaces the generic `ValueError("Down limit nemůže být vyšší než up limit")`
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
This function is used inside `process_down_limit_value`:

1. Normalize the provided value.
2. Check if `down_limit > up_limit`.
3. If yes → call this function.
4. Otherwise return the normalized value.

This ensures:

- consistent validation,
- predictable error handling,
- clear separation of validation and error raising.

---

## Diagnostic value
The error message includes:

- the invalid down limit value,
- the expected maximum (up limit),
- the current instance value,
- the configured up limit,
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