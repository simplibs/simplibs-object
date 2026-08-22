from typing import Any, TYPE_CHECKING
# Outers
from ....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleConstantProtocol


def bool_or_raise_validate_error(
    cls: "SimpleConstantProtocol",
    value: Any,
    problem: str,
    *,
    return_bool: bool = False,
) -> bool:
    """Internal implementation of the shared validation helper."""

    # 1. Boolean mode — return False instead of raising
    if return_bool:
        return False

    # 2. Raise a structured validation error
    raise SimpleRuntimeError(
        error_name="VALIDATION ERROR",
        label="input_value",
        value=value,
        expected=f"Valid configuration for '{cls.__name__}'",
        problem=problem,
        how_to_fix=(
            f"Ensure that the data provided to '{cls.__name__}' meets the validation criteria.",
            f"The expected base type or format is '{cls.meta.value_type_name}'.",
        ),
        context=f"Triggered inside custom validation of '{cls.__name__}'.",
        exception=ValueError,
    )


_DESIGN_NOTES = """
# bool_or_raise_validate_error

## Purpose
Provides a convenience helper for developers implementing custom validation
logic in the `_validate` method of constant classes. It allows users to write
simple, readable validation rules without manually constructing structured
exceptions.

---

## Behavior
1. **Boolean Mode**
   - When `return_bool=True`, the function returns `False` instead of raising an
     error.
   - This supports the boolean-style validation pattern used throughout the
     validation pipeline.

2. **Exception Mode**
   - When `return_bool=False`, the function raises a structured `SimpleRuntimeError`
     containing:
     - the problematic value,
     - a user-provided description of the issue (`problem`),
     - expected type information,
     - contextual information about where the error occurred.

---

## Usage
This helper is intended to be used exclusively inside user-defined `_validate`
methods, for example:

```python
@classmethod
def _validate(cls, value, *, return_bool=False):
    if value < 0:
        return cls.bool_or_raise_validate_error(value, "Value must be non-negative.", return_bool=return_bool)
    return True
"""