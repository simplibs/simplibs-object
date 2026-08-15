from typing import Any, NoReturn
from simplibs.sentinels import UNSET
# Outers
from ....exceptions import SimpleLogicError


def validate_constant_has_default(class_name: str, default: Any) -> None | NoReturn:
    """Validates that a constant leaf class definition provides a valid non-None default value."""

    if default in (UNSET, None):
        raise SimpleLogicError(
            error_name="INVALID CONSTANT DEFAULT ERROR",
            label="constant_missing_or_none_default",
            expected="A valid non-UNSET and non-None default value (default not in (UNSET, None))",
            value=default,
            problem=(
                f"Attempted to create constant class '{class_name}' with an invalid default value ({default!r}). ",
                f"Constant default values cannot be UNSET or None."
            ),
            context=(
                f"Dynamic creator requires a concrete non-None default value for constant '{class_name}' ",
                f"to perform type inference and compute composite default values across node trees."
            ),
            how_to_fix=(
                "Provide a concrete initial value for 'default' (e.g. 0, '', False, or a specific domain object).",
                "Do not use None as a default value — Simple framework trees rely on non-None defaults to derive composite logic.",
                "Supported optional parameters for constants: 'value_type', 'validate'.",
                "If you intended to create a SimpleObject (composite node): provide 'inners' tuple and 'logic' callable instead.",
            ),
            exception=ValueError,
        )


_DESIGN_NOTES = """
# validate_constant_has_default

## Purpose
Enforces the mandatory presence of a concrete, non-None default value when dynamically instantiating 
a `SimpleConstant` class blueprint.

## Behavior
1. Checks if `default` is `UNSET` or `None`.
2. Raises `SimpleLogicError` explaining that `None` is disallowed due to automatic type inference 
   and default value propagation rules across composite object trees.

## Notes
- Strict non-None default enforcement is a core architectural rule of the Simple library.
"""