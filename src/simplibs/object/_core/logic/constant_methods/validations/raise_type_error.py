from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def raise_type_error(
    cls: "SimpleConstantProtocol",
    value: Any,
) -> NoReturn:
    """Raises a detailed user-facing type mismatch error."""

    expected_types = cls.meta.value_type_name
    class_name = cls.__name__

    raise SimpleRuntimeError(
        error_name="TYPE ERROR",
        label="value",
        value=value,
        expected=f"Instance of type '{expected_types}'",
        problem=(
            f"The provided value does not match the required type for constant "
            f"'{class_name}'."
        ),
        context=(
            f"Runtime type enforcement for '{class_name}' requires a value of "
            f"type {expected_types}."
        ),
        how_to_fix=(
            f"Ensure that the provided value is an instance of: {expected_types}.",
            "Check whether any unintended type conversion or transformation "
            "occurs before this validation.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_type_error

## Purpose
Signals that a value passed to a constant definition does not match the expected
type declared in the constant’s metadata. This error is user-facing and explains
why the value cannot be accepted.

## Behavior
- Retrieves the expected type name from metadata.
- Reports the mismatch between the provided value and the required type.
- Raises a structured `SimpleRuntimeError` with clear diagnostics and guidance.

## Notes
- This validation is part of the constant-level API (`validate_type`, `validate`,
  `normalize`).
- The error does not instruct the developer to modify metadata; instead, it
  informs the *user* that the provided value is incompatible.
- Type validation is deterministic and does not perform implicit conversions.
"""