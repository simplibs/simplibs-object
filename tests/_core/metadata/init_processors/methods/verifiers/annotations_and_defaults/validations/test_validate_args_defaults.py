from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from .......protocols.methods import ClassMethodProtocol


def validate_args_defaults(
    expected_args_defaults: tuple[Any, ...],
    expected_params: tuple[str, ...],
    bound_method: "ClassMethodProtocol",
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates positional argument default values."""

    # 1. Extract user-defined positional defaults
    method_args_defaults = bound_method.__func__.__defaults__ or ()

    # 2. Happy path: no defaults declared
    if not method_args_defaults:
        return

    class_name, method_name, context = exception_info

    # 3. Validate each default value
    for index, (value, expected_value) in enumerate(
        zip(method_args_defaults, expected_args_defaults)
    ):
        if value != expected_value:
            param_name = expected_params[index]

            raise SimpleMetadataError(
                error_name="METHOD SIGNATURE ERROR",
                label="_args_default",
                value=value,
                expected=repr(expected_value),
                problem=f"Parameter '{param_name}' has an incorrect default value.",
                context=context,
                how_to_fix=(
                    f"Set the default value of '{param_name}' to '{expected_value}'.",
                    "Or remove the default entirely; the framework will inject it automatically.",
                ) + expected_structure,
                exception=ValueError,
            )


_DESIGN_NOTES = """
# validate_args_defaults

## Purpose
Ensures that positional argument default values match the deterministic defaults
defined in `_inners`.  
Users may omit defaults, but they must never override them.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method-validation helpers.

## Behavior
1. Extract positional defaults from `__defaults__`.
2. If none exist → exit immediately.
3. Compare each default with the expected value.
4. If any mismatch occurs, raise a structured `SimpleMetadataError` with a
   copy‑paste ready blueprint.

## Notes
This validator is part of the annotation/defaults verification chain:
- `validate_annotations`
- `validate_args_defaults`
- `validate_kwargs_defaults`
"""