from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleDefinitionError
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def validate_kwargs_defaults(
    expected_kwargs_defaults: dict[str, Any],
    bound_method: "ClassMethodProtocol",
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates keyword-only argument default values."""

    # 1. Extract user-defined keyword defaults
    method_kwargs_defaults = bound_method.__func__.__kwdefaults__ or {}

    # 2. Happy path: no defaults declared
    if not method_kwargs_defaults:
        return

    class_name, method_name, context = exception_info

    # 3. Validate each keyword default
    for name, value in method_kwargs_defaults.items():
        expected_value = expected_kwargs_defaults.get(name)

        if value != expected_value:
            raise SimpleDefinitionError(
                error_name="METHOD SIGNATURE ERROR",
                label="_kwargs_default",
                value=value,
                expected=repr(expected_value),
                problem=f"Parameter '{name}' has an incorrect default value.",
                context=context,
                how_to_fix=(
                    f"Set the default value of '{name}' to '{expected_value}'.",
                    "Or remove the default entirely; the framework will inject it automatically.",
                ) + expected_structure,
                exception=ValueError,
            )



_DESIGN_NOTES = """
# validate_kwargs_defaults

## Purpose
Ensures that keyword-only argument default values match the deterministic defaults
defined in `_inners`.  
Users may omit defaults, but they must never override them.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method-validation helpers.

## Behavior
1. Extract keyword defaults from `__kwdefaults__`.
2. If none exist → exit immediately.
3. Compare each default with the expected value.
4. If any mismatch occurs, raise a structured `SimpleDefinitionError` with a
   copy‑paste ready blueprint.

## Notes
This validator is part of the annotation/defaults verification chain:
- `validate_annotations`
- `validate_args_defaults`
- `validate_kwargs_defaults`
"""