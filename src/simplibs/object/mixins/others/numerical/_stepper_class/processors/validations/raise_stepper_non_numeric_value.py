from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.instance import SimpleInstanceLike


def raise_stepper_non_numeric_value(
    instance: "SimpleInstanceLike",
    value: Any,
) -> NoReturn:
    """
    Raises a structured error when the instance's value is not numeric.
    Stepper requires numeric values to perform stepping operations.
    """

    raise SimpleLogicError(
        error_name="STEPPER VALUE TYPE ERROR",
        label="instance.value",
        value=value,
        expected="A numeric type (int, float, or any subclass of Number).",
        problem=(
            "The instance's value is not numeric. Stepper operations require "
            "a numeric value to perform increments, decrements, and limit checks."
        ),
        context=(
            f"Instance type: {type(instance).__name__}.",
            f"Received value type: {type(value).__name__!r}.",
            "Stepper can only operate on numeric values that support arithmetic operations."
        ),
        how_to_fix=(
            "Ensure that the instance's `value` attribute is numeric.",
            "If the value comes from a composite calculation, verify that the composite returns a number.",
            "If the value is user-provided, validate or convert it before assigning it to the instance.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_stepper_non_numeric_value

## Purpose
Provides a structured diagnostic error when a Simple instance used by the
Stepper contains a non-numeric value.  
This replaces the generic TypeError with a rich, contextual, and actionable
error message consistent with the Simple ecosystem.

Stepper requires numeric values to perform:

- increments,
- decrements,
- limit checks,
- type-consistent stepping.

Therefore, non-numeric values must be rejected early and clearly.

---

## Architectural reasoning
Stepper is a numerical mixin subsystem.  
Its correctness depends on the assumption that:

```
instance.value is a Number
```

If this assumption is violated:

- arithmetic operations fail,
- limit comparisons break,
- callbacks may misfire,
- the instance may enter an invalid state.

Therefore, the error must:

- clearly explain the violation,
- show the offending value,
- describe what is expected,
- provide actionable steps,
- include contextual information about the instance.

This mirrors the design of immutability, history, metadata, and composite errors.

---

## Pipeline position
This function is used inside `validate_instance`:

1. Check if `instance.value` is numeric.
2. If not → call this function.
3. Otherwise continue with Stepper initialization.

This ensures:

- consistent validation,
- predictable error handling,
- clear separation of validation and error raising.

---

## Diagnostic value
The error message includes:

- the invalid value,
- the expected numeric type,
- the received type,
- the instance type,
- actionable steps to resolve the issue.

This makes debugging significantly easier and aligns with the philosophy of
Simple’s structured error system.

---

## Notes
- This is a pure `raise_...` function: it performs no branching logic.
- It is internal and not part of the public API.
- All non-numeric instance values must use this function.
- The error type is `SimpleLogicError` with `TypeError` as the underlying exception.
"""