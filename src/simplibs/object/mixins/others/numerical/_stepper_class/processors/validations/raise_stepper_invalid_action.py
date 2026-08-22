from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.numerical.stepper import StepperProtocol


def raise_stepper_invalid_action(
    stepper: "StepperProtocol",
    action_value: Any,
) -> NoReturn:
    """
    Raises a structured error when the provided limit action is not callable.
    """

    raise SimpleRuntimeError(
        error_name="STEPPER LIMIT ACTION ERROR",
        label="limit action",
        value=action_value,
        expected="A callable object (function, method, or callable instance).",
        problem=(
            "The provided limit action is not callable. "
            "Stepper limit actions must be executable callbacks."
        ),
        context=(
            f"Instance type: {type(stepper._instance).__name__}.",
            f"Current value: {stepper._instance.value!r}.",
            "Limit actions are executed when the stepper reaches configured boundaries.",
            "Non-callable objects cannot be invoked as callbacks."
        ),
        how_to_fix=(
            "Provide a callable object, such as a function or method.",
            "Ensure that the action does not require arguments when invoked.",
            "If you need a more complex action, wrap it into a callable object.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_stepper_invalid_action

## Purpose
Provides a structured diagnostic error when a user attempts to configure
a limit action that is not callable.  
This replaces the generic `ValueError("Akce musí být volatelný objekt")`
with a rich, contextual, and actionable error message consistent with the
Simple ecosystem.

Limit actions are executed when the stepper reaches its numeric boundaries,
so they must always be valid callable objects.

---

## Architectural reasoning
Stepper supports optional callbacks:

- `up_limit_action`
- `down_limit_action`

These callbacks are executed when the stepper reaches the configured limits.
Because they are invoked automatically, they **must be callable**.

If a non-callable object is provided:

- the callback cannot be executed,
- the stepper may enter an inconsistent state,
- limit handling becomes unpredictable,
- debugging becomes significantly harder.

Therefore, the error must:

- clearly explain the violation,
- show the offending value,
- describe what is expected,
- provide actionable steps,
- include contextual information about the instance.

This mirrors the design of immutability, history, metadata, and composite errors.

---

## Pipeline position
This function is used inside `process_limit_action`:

1. Check if `callable(value)` is false.
2. If yes → call this function.
3. Otherwise return the value unchanged.

This ensures:

- consistent validation,
- predictable error handling,
- clear separation of validation and error raising.

---

## Diagnostic value
The error message includes:

- the invalid action value,
- the expected type (callable),
- the current instance value,
- the instance type,
- actionable steps to resolve the issue.

This makes debugging significantly easier and aligns with the philosophy of
Simple’s structured error system.

---

## Notes
- This is a pure `raise_...` function: it performs no branching logic.
- It is internal and not part of the public API.
- All invalid limit actions must use this function.
- The error type is `SimpleRuntimeError` with `TypeError` as the underlying exception.
"""