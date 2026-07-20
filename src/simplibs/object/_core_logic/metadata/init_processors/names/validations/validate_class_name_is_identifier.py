# Outers
from ......exceptions import SimpleMetadataError


def validate_class_name_is_identifier(
    class_name: str
) -> None:
    """Validates that the class name is a valid Python identifier, catching malformed dynamic types."""
    if not class_name.isidentifier():
        raise SimpleMetadataError(
            error_name="CLASS NAME NOT IDENTIFIER",
            label="Invalid Python name",
            value=class_name,
            problem=f"The class name '{class_name}' is not a valid Python identifier.",
            expected="A valid identifier starting with a letter or underscore, containing only alphanumeric characters and underscores.",
            how_to_fix=(
                "Ensure the class name does not contain spaces, dashes, or dots.",
                "The name must not begin with a digit.",
                "When creating classes dynamically via type(name, ...), verify that the 'name' parameter complies with Python identifier rules.",
            ),
            context="Structural validation of dynamic class identifiers during metadata extraction.",
            exception=ValueError
        )



_DESIGN_NOTES = """
# validate_class_name_is_identifier

## Purpose
This validation acts as a fundamental technical filter for class names. Its primary objective is to guarantee that the blueprint class name adheres strictly to Python's lexical definitions for identifiers before any other processing or name splitting occurs.

## Why This Validation Is Necessary (Dynamic Context)
While standard static definitions (e.g., `class MyClass:`) are checked natively by the Python parser/compiler, dynamic runtime class generation using `type("Invalid-Name", ...)` is highly permissive. It allows creating classes with names containing spaces, hyphens, dots, or names starting with digits.
This function guarantees that even a dynamically spawned class possesses an executable-safe identity name that is technically usable for downstream attribute generation and dynamic code evaluation.

## Validation Pipeline Architecture
Within the metadata initialization sequence, this check serves as the initial guardian before finer filtering takes place. The architectural processing flow follows these three distinct pillars:
1. `validate_class_name_is_identifier` (This function): Eliminates spaces, hyphens, dots, and starting digits. Allows: `[a-zA-Z0-9_]` (including valid Unicode word/diacritic characters).
2. `validate_class_name_is_ascii`: Eliminates localized diacritics and non-ASCII Unicode letters. Allows: `[a-zA-Z0-9_]`.
3. `validate_class_name_has_no_underscores`: Eliminates underscores entirely, establishing a pure PascalCase constraint. Allows: `[a-zA-Z0-9]`.

## Native Python Guarantees
Even during dynamic class creation via `type()`, the Python runtime natively ensures the following (raising TypeError or ValueError automatically before this validation is even reached):
- The incoming class name attribute is always a strict `str` type.
- The incoming string is never an empty value `""`.

## Examples
```python
# VALID (Passes this check, diacritics/underscores handled downstream)
validate_class_name_is_identifier("MyClass")               # OK
validate_class_name_is_identifier("Třída_1")               # OK

# INVALID (Raises SimpleMetadataError via ValueError)
validate_class_name_is_identifier("123Class")              # Fail: starts with a digit
validate_class_name_is_identifier("My-Class")              # Fail: contains a hyphen
validate_class_name_is_identifier("My Class")              # Fail: contains a space
validate_class_name_is_identifier("My.Class")              # Fail: contains a dot

"""