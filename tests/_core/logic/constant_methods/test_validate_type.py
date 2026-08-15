from typing import Any, NoReturn, TYPE_CHECKING
# Inners
from .validations import raise_type_error
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleConstantProtocol


def validate_type(
    cls: "SimpleConstantProtocol",
    value: Any,
    *,
    return_bool: bool = False,
) -> bool | NoReturn:
    """Performs deterministic type validation based on class metadata."""

    # 1. Happy path — value matches expected type
    if isinstance(value, cls.meta.value_type):
        return True

    # 2. Boolean mode — return False instead of raising
    if return_bool:
        return False

    # 3. Raise detailed type mismatch error
    raise_type_error(cls, value)



_DESIGN_NOTES = """
# validate_type

## Purpose
Performs strict, deterministic type validation for constant definitions based on
the type declared in metadata (`meta.value_type`). This function is the first
step in the validation pipeline (`validate_type` → `validate` → `normalize`).

## Behavior
1. Accepts the value if it is an instance of the expected type.
2. Returns `False` when `return_bool=True`.
3. Raises a structured `SimpleLogicError` via `raise_type_error` otherwise.

## Notes
- This function is intentionally minimal; all diagnostic detail is delegated to
  `raise_type_error`.
- The public-facing docstring belongs to the *class method* (`SimpleConstant.validate_type`),
  not to this internal helper.
"""