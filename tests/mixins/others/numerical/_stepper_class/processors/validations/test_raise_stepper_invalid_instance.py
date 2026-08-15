from typing import NoReturn, Any
# Outers
from ......exceptions import SimpleMixinError


def raise_stepper_invalid_instance(
    instance: Any,
    expected_type: type,
) -> NoReturn:
    """
    Raises a structured error when the provided object does not satisfy
    the SimpleInstanceType protocol required by the Stepper.
    """

    raise SimpleMixinError(
        error_name="STEPPER INSTANCE ERROR",
        label="instance",
        value=instance,
        expected=f"Instance implementing {expected_type.__name__}",
        problem=(
            "The provided object does not satisfy the required Simple instance "
            "protocol. The Stepper can only operate on valid Simple instances "
            "that expose a numeric `value` attribute and support mixin operations."
        ),
        context=(
            f"Received type: {type(instance).__name__}.",
            "Stepper requires a Simple instance with a numeric value.",
            "Invalid instances cannot participate in numeric stepping operations."
        ),
        how_to_fix=(
            "Ensure that the object passed to Stepper is a valid Simple instance.",
            "Verify that the instance implements the required protocol.",
            "Check that the instance exposes a numeric `value` attribute.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_stepper_invalid_instance

## Purpose
Provides a structured diagnostic error when a user attempts to initialize
a Stepper with an object that does not satisfy the required Simple instance
protocol.  
This replaces the generic `TypeError("Předaný objekt není validní instancí Simple systému")`
with a rich, contextual, and actionable error message consistent with the
Simple ecosystem.

This protects the Stepper from being attached to invalid or incompatible objects.

---

## Architectural reasoning
Stepper is tightly integrated with Simple instances:

- it reads and writes the instance’s `value`,
- it enforces numeric boundaries,
- it triggers limit actions,
- it participates in mixin initialization.

Therefore, the Stepper **must** be attached only to objects that satisfy the
`SimpleInstanceType` protocol.

If an invalid object is passed:

- numeric operations cannot be performed,
- limit checks break,
- callbacks may fail,
- the instance may enter an inconsistent state.

Therefore, the error must:

- clearly explain the violation,
- show the offending object,
- describe what is expected,
- provide actionable steps,
- include contextual information about the instance.

This mirrors the design of immutability, history, metadata, and composite errors.

---

## Pipeline position
This function is used inside `validate_instance`:

1. Check if `isinstance(instance, SimpleInstanceType)` is false.
2. If yes → call this function.
3. Otherwise continue with numeric validation.

This ensures:

- consistent validation,
- predictable error handling,
- clear separation of validation and error raising.

---

## Diagnostic value
The error message includes:

- the invalid instance object,
- the expected protocol type,
- the received type,
- actionable steps to resolve the issue.

This makes debugging significantly easier and aligns with the philosophy of
Simple’s structured error system.

---

## Notes
- This is a pure `raise_...` function: it performs no branching logic.
- It is internal and not part of the public API.
- All invalid Stepper instance attachments must use this function.
- The error type is `SimpleMixinError` with `TypeError` as the underlying exception.
"""