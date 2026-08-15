from typing import NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleObjectProtocol


def raise_unknown_parameter_error(
    cls: "SimpleObjectProtocol",
    unknown_params: list[str],
) -> NoReturn:
    """Raises an error when unknown keyword parameters are passed to calculate_value."""

    class_name = cls.__name__
    formatted = ", ".join(f"'{p}'" for p in unknown_params)

    raise SimpleLogicError(
        error_name="INVALID PARAMETERS",
        label="kwargs",
        value=formatted,
        expected="Only parameters matching the inner elements of the composite",
        problem=(
            f"The class '{class_name}' does not define the following parameters: "
            f"{formatted}."
        ),
        context=(
            f"During parameter processing for '{class_name}.calculate_value', "
            f"the system detected keyword arguments that do not correspond to "
            f"any inner element."
        ),
        how_to_fix=(
            "Remove the unknown keyword arguments.",
            "Ensure that each keyword argument matches the name of an inner element.",
            "Check the '_inners' definition of the class to see the valid parameter names.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_unknown_parameter_error

## Purpose
Signals that the user passed keyword arguments to `calculate_value` that do not
match any inner element defined in the composite class. This error is user-facing
and prevents silent misuse of the API.

---

## Behavior
- Collects all unknown keyword parameters.
- Raises a structured `SimpleLogicError` describing the mismatch.
- Provides actionable guidance on how to correct the call.

---

## Why this error exists
Composite objects define their structure through `_inners`.  
Each inner element corresponds to one valid parameter name.

If the user passes a keyword argument that does not match any inner:

- the system cannot map the value to an inner element,
- the composite value cannot be computed correctly,
- the call becomes ambiguous or meaningless.

This error ensures predictable behavior and prevents silent failures.

---

## Notes
- Used inside `process_calculate_value_params`.
- The public-facing documentation belongs to `SimpleObject.calculate_value`.
- Uses `ValueError` as the underlying exception type for consistency with Python’s
  argument handling semantics.
"""