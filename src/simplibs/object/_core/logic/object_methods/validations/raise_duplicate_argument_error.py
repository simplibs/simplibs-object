from typing import NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleObjectProtocol


def raise_duplicate_argument_error(
    cls: "SimpleObjectProtocol",
    param_name: str,
) -> NoReturn:
    """Raises an error when an argument is provided both positionally and by keyword."""

    class_name = cls.__name__

    raise SimpleRuntimeError(
        error_name="INVALID PARAMETERS",
        label=param_name,
        value=f"Positional and keyword argument for '{param_name}'",
        expected=f"Parameter '{param_name}' provided either positionally OR as a keyword",
        problem=(
            f"The parameter '{param_name}' was supplied twice when calling "
            f"'{class_name}.calculate_value': once as a positional argument and "
            f"once as a keyword argument."
        ),
        context=(
            f"During parameter processing for '{class_name}.calculate_value', "
            f"the system detected a duplicate argument definition."
        ),
        how_to_fix=(
            "Provide the parameter only once.",
            "If you prefer positional arguments, remove the keyword version.",
            "If you prefer keyword arguments, remove the positional version.",
            "Ensure that each inner element is mapped to exactly one argument.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_duplicate_argument_error

## Purpose
Signals that a parameter was supplied both positionally and as a keyword when
calling `calculate_value`. This is a user-facing error that prevents ambiguous
argument mapping in composite objects.

---

## Behavior
- Detects when the same parameter name appears in both `args` and `kwargs`.
- Raises a structured `SimpleRuntimeError` explaining the conflict.
- Provides actionable guidance on how to correct the call.

---

## Why this error exists
Composite objects map positional arguments to inner elements **by order**.  
Keyword arguments map them **by name**.

If a parameter is supplied twice:

- the system cannot determine which value should be used,
- the mapping becomes ambiguous,
- the resulting composite value could be incorrect.

This error ensures predictable behavior and prevents silent overwrites.

---

## Notes
- Used inside `process_calculate_value_params`.
- The public-facing documentation belongs to `SimpleObject.calculate_value`.
- Uses `ValueError` as the underlying exception type for consistency with Python’s
  argument handling semantics.
"""