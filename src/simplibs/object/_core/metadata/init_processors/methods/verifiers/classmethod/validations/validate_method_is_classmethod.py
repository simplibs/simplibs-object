from typing import Any
# Outers
from ........exceptions import SimpleDefinitionError


def validate_method_is_classmethod(
    raw_method: Any,
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that the method is decorated with @classmethod."""

    if not isinstance(raw_method, classmethod):
        class_name, method_name, context = exception_info

        raise SimpleDefinitionError(
            error_name="METHOD LOGIC ERROR",
            label="_method",
            value=raw_method,
            problem=f"'{class_name}.{method_name}' is not a classmethod.",
            expected="A method decorated with '@classmethod'.",
            how_to_fix=(
                f"Add '@classmethod' to '{method_name}'.",
                "Without this decorator, the system cannot bind the method correctly.",
            ) + expected_structure,
            context=context,
            exception=TypeError,
        )


_DESIGN_NOTES = """
# validate_method_is_classmethod

## Purpose
Ensures that the reflected method is explicitly decorated with `@classmethod`.
The metadata pipeline relies on class‑bound semantics, so instance methods or
plain attributes cannot be used.

## Why tuple inputs
The validator receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function consistent with all other method‑validation helpers.

## Behavior
If the raw attribute is not a `classmethod` instance, the validator raises a
structured `SimpleDefinitionError` containing:
- the class and method name,
- a clear explanation of the issue,
- a copy‑paste ready blueprint showing the correct method layout.

## Notes
This validator is used for all three method types:
- `_validate`
- `_logic`
- `_decompose`

It is the third guard in the classmethod verification chain.
"""