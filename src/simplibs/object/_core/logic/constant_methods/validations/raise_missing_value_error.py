from typing import TYPE_CHECKING, NoReturn
# Outers
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def raise_missing_value_error(
    cls: "SimpleConstantProtocol",
) -> NoReturn:
    """Raises an error when None is provided where a valid value is required."""

    class_name = cls.__name__
    expected_type = cls.meta.value_type_name

    raise SimpleRuntimeError(
        error_name="MISSING VALUE ERROR",
        label="value",
        value=None,
        expected=f"A valid instance of type '{expected_type}' (not None)",
        problem=f"The class '{class_name}' requires a concrete value, but received None.",
        context=(
            f"Normalization phase for '{class_name}' rejected a None value because "
            f"None is not permitted in the SimpleObject ecosystem."
        ),
        how_to_fix=(
            "Provide a valid value or an instance of the required type.",
            "If you want the system to automatically substitute the default value "
            "when None is provided, call the method with 'process_none=True'.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_missing_value_error

## Purpose
Signals that a `None` value was provided where a valid, non-null value is
required. This error is user-facing and explains why `None` cannot be accepted
during normalization.

---

## Why `None` is forbidden
The SimpleObject ecosystem does not allow `None` as a valid runtime value:

- Composite objects compute their value from inner elements.
- If any inner element were `None`, the composite value could not be computed.
- Metadata prevents `None` from being used as a declared default.
- `normalize` enforces this rule at runtime for user-provided values.

The only exception is when `process_none=True`, which instructs the system to
replace `None` with the class’s default value.

---

## Behavior
- Always raises a structured `SimpleRuntimeError`.
- Explains that the class requires a concrete value.
- Provides guidance on how to use `process_none=True` when appropriate.

---

## Notes
- This function is used exclusively by `normalize`.
- The public-facing documentation belongs to `SimpleConstant.normalize`, not to
  this internal helper.
- The error message is intentionally concise and user-oriented.
"""