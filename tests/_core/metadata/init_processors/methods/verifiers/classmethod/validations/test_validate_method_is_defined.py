from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def validate_method_is_defined(
    method_name: str,
    owner_class: "SimpleClassLike",
    exception_info: tuple[str, str, str],
    expected_structure: tuple[str, ...],
) -> None:
    """Validates that the method is defined directly on the class."""

    if method_name not in owner_class.__dict__:
        class_name, _, context = exception_info

        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="_method",
            value=method_name,
            problem=f"Class '{class_name}' does not define this method.",
            expected=f"Method '{method_name}' must be declared in class '{class_name}'.",
            how_to_fix=(
                f"Add '{method_name}' directly to the class definition.",
                "Decorate it with '@classmethod'.",
                "Ensure its parameters match the expected signature.",
            ) + expected_structure,
            context=context,
            exception=AttributeError,
        )


_DESIGN_NOTES = """
# validate_method_is_defined

## Purpose
Ensures that the class explicitly defines the method in its own namespace.
The check uses `owner_class.__dict__` to avoid inherited methods and detect
missing overrides reliably.

## Why tuple inputs
The validation receives:
- `exception_info` — (class_name, method_name, context)
- `expected_structure` — code blueprint

This keeps the function simple, fast, and consistent with all other
exception‑helpers in the metadata pipeline.

## Behavior
If the method is not found in `__dict__`, the validator raises a structured
`SimpleMetadataError` containing:
- the missing method name,
- the class name,
- a clear explanation,
- a copy‑paste ready blueprint showing the correct method layout.

## Notes
This validator is used for all three method types:
- `_validate`
- `_logic`
- `_decompose`

It is the first guard in the classmethod verification chain.
"""