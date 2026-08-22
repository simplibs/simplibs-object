from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from ........exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ........_core.protocols.mixins.numerical.stepper import StepperProtocol


def raise_stepper_up_limit_reached(
    stepper: "StepperProtocol",
    new_value: Any,
) -> NoReturn:
    """
    Raises a structured error when a step operation attempts to exceed
    the configured upper limit.
    """

    raise SimpleRuntimeError(
        error_name="STEPPER UP LIMIT ERROR",
        label="new value",
        value=new_value,
        expected=f"Value <= {stepper.up_limit!r}",
        problem=(
            "The step operation attempted to increase the value above the "
            "configured upper limit."
        ),
        context=(
            f"Instance type: {type(stepper._instance).__name__}.",
            f"Current value: {stepper._instance.value!r}.",
            f"Upper limit: {stepper.up_limit!r}.",
            "The stepper enforces numeric boundaries to prevent invalid state transitions."
        ),
        how_to_fix=(
            "Increase the upper limit if higher values should be allowed.",
            "Adjust the step value to avoid crossing the limit.",
            "Disable limit enforcement if this behavior is intentional.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_stepper_up_limit_reached

## Purpose
Provides a structured diagnostic error when a step operation attempts to move
the value above the configured upper limit.  
This replaces the generic `ValueError("Dosaženo horního limitu")` with a rich,
contextual, and actionable error message consistent with the Simple ecosystem.

The function ensures that upper‑limit violations are always reported clearly
and predictably.

---

## Architectural reasoning
Stepper is responsible for safe numeric manipulation.  
Crossing the upper limit is a **logical violation** of the stepper’s
configuration, not just a numeric mismatch.

Therefore, the error must:

- explain what happened,
- show the offending value,
- show the configured limit,
- provide actionable steps,
- include contextual information about the instance.

This mirrors the design of immutability, history, metadata, and composite
errors.

---

## Pipeline position
This function is used inside `verify_up_limit`:

1. Check if `new_value > up_limit`.
2. Trigger `up_limit_action` if present.
3. If `raise_exception=True`, call this function.
4. Otherwise return `False`.

This ensures:

- consistent behavior across all step operations,
- predictable error handling,
- clear separation of validation and error raising.

---

## Diagnostic value
The error message includes:

- the invalid new value,
- the expected maximum value,
- the current instance value,
- the configured upper limit,
- the instance type,
- actionable steps to resolve the issue.

This makes debugging significantly easier and aligns with the philosophy of
Simple’s structured error system.

---

## Notes
- This is a pure `raise_...` function: it performs no branching logic.
- It is internal and not part of the public API.
- All stepper limit violations must use this function.
- The error type is `SimpleRuntimeError` with `ValueError` as the underlying exception.
"""