from typing import Any, NoReturn
# Outers
from ....exceptions import SimpleDefinitionError


def validate_class_name_is_str(class_name: Any) -> None | NoReturn:
    """Validates that class_name is a non-empty string."""

    if isinstance(class_name, str) and class_name.strip():
        return

    raise SimpleDefinitionError(
        error_name="INVALID CLASS NAME ERROR",
        label="class_name_is_not_str",
        expected="A non-empty string for class name definition",
        value=type(class_name).__name__,
        problem=f"Provided class name must be a non-empty string. Received type '{type(class_name).__name__}'.",
        context="Attempted to dynamically generate a class blueprint, but 'class_name' validation failed.",
        how_to_fix=(
            "Pass a valid string for 'class_name', e.g. class_name='MyCustomConstant'.",
            "Ensure class_name is not empty or whitespace-only.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_class_name_is_str

## Purpose
Guarantees that the target name for dynamically generated classes is a valid non-empty string.

## Behavior
1. Checks if `class_name` is an instance of `str` and contains non-whitespace characters.
2. Raises `SimpleDefinitionError` wrapping `TypeError` if invalid.
"""