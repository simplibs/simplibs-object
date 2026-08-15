from typing import Any, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.mixins.numerical.stepper import StepperProtocol


def process_value(
    self: "StepperProtocol",
    value: Any,
    *,
    validate: bool = True
) -> Any:
    """
    Normalizes and optionally validates a value for use in the stepper.

    Converts the provided value to the correct instance type and optionally
    validates it using the instance’s validation logic.
    """

    # 1. Normalize the value
    _value = (
        value if isinstance(value, self._value_type)
        else self._value_type(value)
    )

    # 2. Validate the value
    if validate:
        self._instance.validate(_value)

    # 3. Return the normalized value
    return _value


_DESIGN_NOTES = """
# process_value

## Purpose
Normalizes and optionally validates a value before it is used by the stepper.
This function ensures that:

- the value is converted to the correct numeric type,
- the value is compatible with the instance’s validation rules,
- stepper operations always work with type‑consistent, validated values.

It provides the canonical logic for preparing values used in stepping,
limit configuration, and direct value assignment.

---

## Architectural role
`process_value` is used by:

- `process_step_value`
- `process_down_limit_value`
- `process_up_limit_value`
- `set_value`
- `step_up`
- `step_down`

It acts as the normalization and validation layer for all numeric inputs
entering the stepper pipeline.

The function integrates with:

- the instance’s `_value_type` for type conversion,
- the instance’s `validate` method for semantic validation,
- optional validation toggling via the `validate` parameter.

---

## How it works

### 1. Type normalization
The function converts the provided value into the instance’s numeric type:

```
self._value_type(value)
```

This ensures:

- type consistency across all stepper operations,
- predictable arithmetic behavior,
- compatibility with limit comparisons.

If the value is already of the correct type, it is used unchanged.

### 2. Optional validation
If `validate=True`, the function calls:

```
self._instance.validate(_value)
```

This allows the instance to enforce:

- custom numeric constraints,
- domain‑specific rules,
- semantic correctness.

Validation is optional because some internal operations (e.g., limit checks)
may require normalization without semantic validation.

### 3. Returning the normalized value
The normalized (and optionally validated) value is returned for further use.

---

## Why this function exists
Stepper operations must work with values that are:

- type‑consistent,
- semantically valid,
- safe for arithmetic operations.

This function encapsulates:

- normalization,
- optional validation,
- deterministic return behavior.

It ensures that invalid or inconsistent values never reach deeper layers of
the stepper pipeline.

---

## Deterministic behavior
The function guarantees:

- stable normalization,
- predictable validation,
- deterministic return values.

This determinism is essential for safe numeric stepping.

---

## Notes
- This function is internal and not part of the public API.
- All structural logic is delegated to instance‑level validation and type conversion.
- The function is intentionally minimal and side‑effect‑free.
"""