from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .process_value import process_value
from .validations import raise_stepper_invalid_down_limit
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.numerical.stepper import StepperProtocol


def process_down_limit_value(
    self: "StepperProtocol",
    value: Any
) -> Any:
    """
    Prepares and validates the down‑limit value for the stepper.

    Normalizes the provided value to the correct type and verifies
    that the down limit is not higher than the currently configured up limit.
    """

    # 1. Normalize the value
    _value = process_value(self, value)

    # 2. Validate boundary consistency
    if self.up_limit is not UNSET and self.up_limit < _value:
        raise_stepper_invalid_down_limit(self, value)

    return _value


_DESIGN_NOTES = """
# process_down_limit_value

## Purpose
Normalizes and validates the down‑limit value for the stepper.  
This function ensures that:

- the provided limit value is converted to the correct numeric type,
- the down limit does not exceed the currently configured up limit (if one is set),
- invalid configurations are rejected early using structured errors.

It provides the canonical logic for configuring the lower numeric boundary.

---

## Architectural role
`process_down_limit_value` is used by the setter:


```

Stepper.down_limit = ...

```

It acts as the validation and normalization layer for down‑limit configuration.

The function integrates with:

- `process_value` for type normalization,
- `raise_stepper_invalid_down_limit` for structured error reporting,
- UNSET semantics for optional limit configuration.

---

## How it works

### 1. Value normalization
The function first calls:


```

_value = process_value(self, value)

```

This ensures:

- type consistency with the instance’s numeric type,
- optional validation,
- safe conversion of user‑provided values.

### 2. Boundary consistency check
The function verifies:


```

self.up_limit is not UNSET and self.up_limit < _value

```

If `up_limit` is configured and is strictly lower than the requested down limit,
the configuration is invalid because:


```

down_limit must be <= up_limit

```

If `up_limit` is UNSET, the boundary check is skipped safely.
Violations are reported using a structured diagnostic error.

### 3. Returning the normalized value
If validation succeeds, the normalized value is returned and stored as the new
down limit.

---

## Why this function exists
Stepper requires consistent numeric boundaries to operate safely.  
This function encapsulates:

- normalization,
- boundary validation respecting UNSET states,
- structured error raising.

It ensures that invalid configurations never reach deeper layers of the stepper
pipeline.

---

## Deterministic behavior
The function guarantees:

- stable normalization,
- predictable validation,
- consistent error raising,
- deterministic return values.

This determinism is essential for safe numeric stepping.

---

## Notes
- This function is internal and not part of the public API.
- All structural logic is delegated to normalization and validation utilities.
- The function is intentionally minimal and side‑effect‑free.
"""