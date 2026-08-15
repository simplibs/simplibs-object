from typing import Any
# Outers
from ........exceptions import SimpleDefinitionError


def validate_method_is_callable(
    raw_method: Any,
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that the reflected method is callable."""

    if not callable(raw_method):
        class_name, method_name, context = exception_info

        raise SimpleDefinitionError(
            error_name="METHOD LOGIC ERROR",
            label="_method",
            value=raw_method,
            problem=f"'{class_name}.{method_name}' is not callable.",
            expected="A callable classmethod.",
            how_to_fix=(
                f"Ensure '{method_name}' is defined as a function.",
                "Verify it was not overwritten by a data attribute.",
            ) + expected_structure,
            context=context,
            exception=TypeError,
        )


_DESIGN_NOTES = """
# validate_method_is_callable

## Purpose
Ensures that the reflected class attribute is a callable object.  
This prevents signature validation from running on non‑callable values such as
strings, integers, or accidental data attributes.

## Why tuple inputs
The function receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the validator consistent with all other method‑validation helpers.

## Behavior
If `callable(raw_method)` is false, the validator raises a structured
`SimpleDefinitionError` containing:
- the class and method name,
- a clear explanation of the issue,
- a copy‑paste ready blueprint showing the correct method layout.

## Notes
This validator is used for all three method types:
- `_validate`
- `_logic`
- `_decompose`

It is the second guard in the classmethod verification chain.
"""