from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from .....exceptions import SimpleRuntimeError
# Inners
from ._extract_clean_code_lines import _extract_clean_code_lines
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleConstantProtocol


def raise_validation_error(
    cls: "SimpleConstantProtocol",
    value: Any,
) -> NoReturn:
    """Raises a standardized error when user-defined validation returns False."""

    # 1. Extract user-defined validation logic
    # noinspection PyBroadException
    try:
        validate_method = cls.meta.validate
        validate_func = getattr(validate_method, "__func__", validate_method)
        validate_source_list = _extract_clean_code_lines(validate_func)
    except Exception:
        validate_source_list = ["    <source code not available>"]

    # 2. Raise structured validation failure error
    raise SimpleRuntimeError(
        error_name="VALIDATION ERROR",
        label="value",
        value=value,
        expected="A value that satisfies the user-defined validation logic.",
        problem="The provided value did not pass the user-defined validation rules.",
        context=(
            f"The '_validate' method of '{cls.__name__}' returned False, indicating "
            f"that the value does not meet the required validation criteria."
        ),
        how_to_fix=(
            "Review the validation logic shown below to understand why the value "
            "was rejected:",
            *validate_source_list,
            "Ensure that the input value matches the assumptions and constraints "
            "defined in your validation method.",
            "If you intend to raise custom validation errors instead of returning "
            "False, use 'SimpleObjectError' or 'cls.bool_or_raise_validate_error()'.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_validation_error

## Purpose
Handles the case where user-defined validation (`_validate`) returns `False`
instead of raising an exception. This error is user-facing and explains that the
value failed the validation rules defined by the developer.

## Behavior
- Extracts the body of the `_validate` method using `extract_clean_code_lines`.
- Displays the validation logic directly in the error message.
- Raises a structured `SimpleRuntimeError` indicating that the value did not meet
  the validation criteria.

## Why this exists
Users may implement `_validate` in two ways:
1. **Boolean style** — return `True` or `False`.
2. **Exception style** — raise `SimpleObjectError` or a subclass.

This function handles the first case, providing a clear and helpful error message
when `_validate` returns `False`.

## Notes
- The extracted code helps users understand exactly which part of their logic
  rejected the value.
- If the source code cannot be retrieved, a placeholder is shown.
- This function is part of the main validation pipeline:
  `validate_type` → `validate` → `raise_validation_error`.
"""