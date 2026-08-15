from typing import TYPE_CHECKING
from numbers import Number
# Outers
from ....._core.protocols.instance import SimpleInstanceType
# Inners
from .validations import (
    raise_stepper_invalid_instance,
    raise_stepper_non_numeric_value
)
# Annotations
if TYPE_CHECKING:
    from ....._core.protocols.instance import SimpleInstanceLike


def validate_instance(
    instance: "SimpleInstanceLike"
) -> None:
    """
    Validates that the provided instance is suitable for use with the stepper.

    Ensures that the instance implements the SimpleInstanceType protocol
    and that its value supports numeric operations.
    """

    # 1. Validate instance protocol
    if not isinstance(instance, SimpleInstanceType):
        raise_stepper_invalid_instance(instance, SimpleInstanceType)

    # 2. Validate that the instance value is numeric
    if not isinstance(instance.value, Number):
        raise_stepper_non_numeric_value(instance, instance.value)


_DESIGN_NOTES = """
# validate_instance

## Purpose
Ensures that the object passed to the Stepper is a valid Simple instance
with a numeric value.  
This function is the first and most fundamental validation step in the Stepper
initialization pipeline.

It guarantees that Stepper is only attached to objects that:

- implement the required SimpleInstanceType protocol,
- expose a numeric `value` attribute,
- support safe numeric stepping operations.

---

## Architectural role
`validate_instance` is called directly from the Stepper constructor:

```
Stepper(instance)
```

It acts as the gateway validation layer for all Stepper operations.

The function integrates with:

- `raise_stepper_invalid_instance` for protocol validation,
- `raise_stepper_non_numeric_value` for numeric validation.

Without this function, Stepper could be attached to invalid objects, leading to
runtime errors and inconsistent behavior.

---

## How it works

### 1. Protocol validation
The function checks:

```
isinstance(instance, SimpleInstanceType)
```

This ensures that the instance:

- exposes a `value` attribute,
- supports mixin initialization,
- participates in Simple’s object model.

If the check fails, a structured diagnostic error is raised.

### 2. Numeric value validation
The function checks:

```
isinstance(instance.value, Number)
```

This ensures that the instance’s value supports:

- arithmetic operations,
- limit comparisons,
- type‑consistent stepping.

If the check fails, a structured diagnostic error is raised.

---

## Why this function exists
Stepper relies on strict assumptions:

- the instance must be a Simple object,
- the value must be numeric,
- the instance must support mixin behavior.

This function enforces these assumptions early and clearly.

It prevents:

- invalid state transitions,
- broken limit checks,
- incorrect arithmetic operations,
- unpredictable callback behavior.

---

## Deterministic behavior
The function guarantees:

- stable protocol validation,
- predictable numeric validation,
- consistent error raising.

This determinism is essential for safe numeric stepping.

---

## Notes
- This function is internal and not part of the public API.
- All structural logic is delegated to validation utilities.
- The function is intentionally minimal and side‑effect‑free.
"""