from typing import TYPE_CHECKING, Any
# Inners
from ._process_calculate_value_params import _process_calculate_value_params
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleObjectProtocol


def calculate_value(
    cls: "SimpleObjectProtocol",
    *args,
    **kwargs,
) -> Any:
    """Computes the composite value by invoking the user-defined `_logic` method."""

    # 1. Process incoming parameters
    params_dict = _process_calculate_value_params(cls, *args, **kwargs)

    # 2. Compute the value using the class's logic function
    outcome = cls.meta.logic(cls, **params_dict)

    # 3. Return the computed value
    return outcome


_DESIGN_NOTES = """
# calculate_value

## Purpose
Serves as the public-facing entry point for computing the value of a composite
object. It connects user-provided parameters with the class’s `_logic` method,
ensuring correct parameter mapping, validation, and execution.

---

## Pipeline Overview

### 1. Parameter Processing
All positional and keyword arguments are normalized and validated through
`_process_calculate_value_params`. This step ensures:

- correct mapping to inner elements,
- default value substitution,
- validation of each inner value,
- structured error reporting for invalid parameters.

### 2. Logic Execution
After parameters are processed, the function invokes:

```
cls.meta.logic(cls, **params_dict)
```

This calls the user-defined `_logic` method with:

- the class itself (`cls`) as the first argument,
- validated parameters as keyword arguments.

### 3. Result Delivery
The return value of `_logic` becomes the composite’s computed value.

---

## Why this function exists
Composite objects must compute their value dynamically based on inner elements.
This function provides:

- a stable API for users,
- full type inference via `ParamSpec`,
- predictable behavior,
- separation of concerns (parameter processing vs. logic execution).

---

## Notes
- This function is attached to `SimpleObject` as a class method.
- The public-facing documentation belongs to `SimpleObject.calculate_value`.
- All diagnostics are delegated to `_process_calculate_value_params` and the
  validation pipeline.
```
"""