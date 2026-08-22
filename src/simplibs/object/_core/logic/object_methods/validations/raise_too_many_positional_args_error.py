from typing import NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleObjectProtocol


def raise_too_many_positional_args_error(
    cls: "SimpleObjectProtocol",
    given_count: int,
    allowed_count: int,
) -> NoReturn:
    """Raises an error when too many positional arguments are passed to calculate_value."""

    class_name = cls.__name__

    raise SimpleRuntimeError(
        error_name="INVALID PARAMETERS",
        label="args",
        value=f"{given_count} positional arguments",
        expected=f"At most {allowed_count} positional arguments matching inner elements",
        problem=(
            f"The class '{class_name}' received more positional arguments than "
            f"the number of defined inner elements."
        ),
        context=(
            f"During parameter processing for '{class_name}.calculate_value', the "
            f"system detected an argument count mismatch."
        ),
        how_to_fix=(
            f"Provide no more than {allowed_count} positional arguments.",
            "If you intended to use named parameters, pass them as keyword arguments.",
            "Ensure that each positional argument corresponds to an inner element "
            "in the order defined by the class.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_too_many_positional_args_error

## Purpose
Signals that the user passed more positional arguments to `calculate_value` than
the number of inner elements defined in the composite class. This error is
user-facing and helps developers understand how to correctly supply parameters
to composite objects.

---

## Behavior
- Compares the number of provided positional arguments with the number of
  declared inner elements.
- Raises a structured `SimpleRuntimeError` when the count exceeds the allowed
  limit.
- Explains the mismatch and provides actionable guidance.

---

## Why this error exists
Composite objects define their structure through `_inners`.  
Each inner corresponds to one parameter of `_logic`.

Passing more positional arguments than inner elements indicates a misuse of the
API — either:

- the user misunderstood the order of parameters, or  
- they intended to use keyword arguments instead.

This error ensures the system remains predictable and prevents silent failures.

---

## Notes
- This function will be used inside `process_calculate_value_params`.
- The public-facing documentation belongs to `SimpleObject.calculate_value`,
  not to this internal helper.
- The error uses `ValueError` as the underlying exception type for consistency
  with Python’s parameter handling semantics.
"""