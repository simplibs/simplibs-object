# Outers
from ......exceptions import SimpleDefinitionError


def validate_class_name_is_identifier(
    class_name: str
) -> None:
    """Validates that the class name is a valid Python identifier."""

    # 1. Check identifier validity
    if class_name.isidentifier():
        return

    # 2. Raise structured metadata error
    raise SimpleDefinitionError(
        error_name="CLASS NAME NOT IDENTIFIER",
        label="class name",
        value=class_name,
        problem=(
            f"The name '{class_name}' is not a valid Python identifier.",
        ),
        expected="A name using only letters, digits, and underscores.",
        how_to_fix=(
            "Remove spaces, hyphens, dots, or other special characters.",
            "Ensure the name does not start with a digit.",
            "If creating classes dynamically via type(name, ...), verify the name first.",
        ),
        context="Identifier validation during metadata name processing.",
        exception=ValueError
    )




_DESIGN_NOTES = """
# validate_class_name_is_identifier

## Purpose
Ensures that the class name follows Python’s strict identifier rules before any
metadata processing begins. This protects the naming pipeline from malformed
dynamic class names.

## Why this validation exists
Static class definitions (`class MyClass:`) are checked by Python automatically.
Dynamic class creation (`type("Bad-Name", ...)`) is not. Python allows names
containing spaces, hyphens, dots, or names starting with digits.

This validator guarantees that even dynamically generated classes have a safe,
usable name.

## Validation pipeline
This function is the first step in a three‑stage name validation sequence:

1. **validate_class_name_is_identifier**  
   Removes names with spaces, hyphens, dots, or leading digits.  
   Allows: `[a-zA-Z0-9_]` including Unicode letters.

2. **validate_class_name_is_ascii**  
   Removes diacritics and non‑ASCII characters.  
   Allows: `[a-zA-Z0-9_]`.

3. **validate_class_name_has_no_underscores**  
   Removes underscores entirely.  
   Enforces pure PascalCase.  
   Allows: `[a-zA-Z0-9]`.

## Native Python guarantees
Python ensures:
- the class name is always a `str`,
- the name is never empty.

## Examples

### Valid
- `"MyClass"`
- `"Trida_1"` (diacritics handled later)

### Invalid
- `"123Class"` — starts with a digit  
- `"My-Class"` — contains a hyphen  
- `"My Class"` — contains a space  
- `"My.Class"` — contains a dot
"""