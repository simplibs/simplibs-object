from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.numerical.stepper import StepperProtocol


def raise_stepper_down_limit_reached(
    stepper: "StepperProtocol",
    new_value: Any,
) -> NoReturn:
    """
    Raises a structured error when a step operation attempts to go below
    the configured down limit.
    """

    raise SimpleMixinError(
        error_name="STEPPER DOWN LIMIT ERROR",
        label="new value",
        value=new_value,
        expected=f"Value >= {stepper.down_limit!r}",
        problem=(
            "The step operation attempted to decrease the value below the "
            "configured down limit."
        ),
        context=(
            f"Instance type: {type(stepper._instance).__name__}.",
            f"Current value: {stepper._instance.value!r}.",
            f"Down limit: {stepper.down_limit!r}.",
            "The stepper enforces numeric boundaries to prevent invalid state transitions."
        ),
        how_to_fix=(
            "Increase the down limit if lower values should be allowed.",
            "Adjust the step value to avoid crossing the limit.",
            "Disable limit enforcement if this behavior is intentional.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_stepper_down_limit_reached

## Purpose
Provides a structured diagnostic error when a step operation attempts to move
the value below the configured down limit.  
This replaces the generic `ValueError` with a rich, contextual, and actionable
error message consistent with the rest of the Simple ecosystem.

The function ensures that limit violations are always reported clearly and
predictably.

---

## Architectural reasoning
Stepper is a numerical mixin subsystem responsible for:

- controlled value manipulation,
- enforcing numeric boundaries,
- triggering limit actions,
- maintaining safe state transitions.

Crossing the down limit is not a trivial numeric error — it is a **logical
violation of the stepper’s configuration**.  
Therefore, it must be reported using a structured error that:

- explains what happened,
- shows the offending value,
- shows the configured limit,
- provides actionable steps to fix the issue,
- includes contextual information about the instance.

This mirrors the design of immutability, history, metadata, and composite
errors.

---

## Pipeline position
This function is used inside `verify_down_limit`:

1. Check if `new_value < down_limit`.
2. Trigger `down_limit_action` if present.
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
- the expected minimum value,
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
- All stepper limit violations must use this function.
- The error type is `SimpleMixinError` with `ValueError` as the underlying exception.
"""