from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...processors import process_value
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.numerical.stepper import StepperProtocol


def process_step_value(
    self: "StepperProtocol",
    value: Any = UNSET,
    *,
    validate: bool = True
) -> Any:
    """
    Prepares and normalizes the step value for use in step_up and step_down.

    If the value is UNSET, returns the default step of the stepper.
    If the value is provided, it undergoes standard normalization and optional validation.
    """
    return (
        self._step if value is UNSET
        else process_value(self, value, validate=validate)
    )


_DESIGN_NOTES = """
# process_step_value

## Purpose
Normalizes and prepares the step value used by `step_up` and `step_down`.
This function ensures that both default step values and user‑provided step
values behave consistently and safely.

It acts as a lightweight wrapper around `process_value`, adding logic specific
to stepper semantics.

## Architectural role
`process_step_value` is used by:

- `step_up`
- `step_down`

It provides the canonical way to interpret the “step amount” before applying
it to the instance’s value.

## How it works
The function performs two deterministic operations:

### 1. Default step handling
If the caller does not provide a step value (`value is UNSET`), the function
returns the stepper’s configured default step (`self._step`).

This ensures that step operations always have a valid numeric increment.

### 2. Normalization of user‑provided step values
If the caller provides a step value, it is passed to `process_value`, which:

- converts the value to the correct numeric type,
- validates the value if requested,
- ensures type consistency with the instance’s value type.

This guarantees that user‑provided step values behave identically to default
step values.

## Integration requirements
The function assumes:

- **StepperProtocol**  
  Provides `_step` and metadata about the instance.

- **process_value**  
  Performs normalization and optional validation of numeric values.

Without these components, step value processing cannot operate correctly.

## Why this function exists
Stepper operations must support:

- default step values,
- user‑provided step values,
- type‑safe normalization,
- optional validation,
- consistent behavior across all numeric types.

This function encapsulates the minimal logic required to achieve that.

## Deterministic behavior
The function guarantees:

- stable fallback to default step,
- predictable normalization,
- consistent validation behavior,
- type‑safe numeric operations.

This determinism is essential for safe stepper behavior.

## Stability guarantee
Any change to this function would affect:

- step_up / step_down semantics,
- numeric consistency,
- validation behavior,
- user experience when stepping values.

Therefore, `process_step_value` is treated as a **core invariant** of the
Stepper subsystem.

## Notes
- This function is intentionally minimal and side‑effect‑free.
- It is not part of the public API; it is used internally by Stepper methods.
- All structural logic is delegated to `process_value`.
"""