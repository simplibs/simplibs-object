# Outers
from ......exceptions import SimpleDefinitionError


def validate_class_name_has_no_underscores(
    class_name: str
) -> None:
    """Validates that the class name contains no underscores."""

    # 1. Check underscore presence
    if "_" not in class_name:
        return

    # 2. Raise structured metadata error
    raise SimpleDefinitionError(
        error_name="CLASS NAME CONTAINS UNDERSCORE",
        label="class name",
        value=class_name,
        problem=(
            "The name contains an underscore (_).",
        ),
        expected="Only alphanumeric characters (A–Z, a–z, 0–9).",
        how_to_fix=(
            "Remove all underscores from the class name.",
            "Use PascalCase (e.g., 'My_Class' → 'MyClass').",
            "Underscores are reserved for internal metadata and generated identifiers.",
        ),
        context="Underscore validation during metadata name processing.",
        exception=ValueError
    )



_DESIGN_NOTES = """
# validate_class_name_has_no_underscores

## Purpose
Ensures that the class name contains no underscore characters.  
This rule is applied after the identifier and ASCII checks, when the remaining
allowed character set is already narrowed down.

The SimpleObject architecture reserves underscores for internal metadata,
private attributes, and generated identifiers. Allowing them in user-defined
class names could cause naming collisions or ambiguity.

## Why this validation exists
Class names are used to derive:
- internal slot names,
- private attributes,
- blueprint paths,
- dynamic identifiers.

If a user-defined class name contains underscores, it may collide with
framework-generated names (e.g., `_value`, `_inner`, `_my_class`).

Removing underscores ensures a clean, predictable PascalCase blueprint.

## Position in the validation pipeline
This is the third step in the name validation sequence:

1. `validate_class_name_is_identifier`  
   Removes illegal symbols, spaces, hyphens, dots, and leading digits.

2. `validate_class_name_is_ascii`  
   Removes diacritics and non-ASCII characters.

3. `validate_class_name_has_no_underscores`  
   Removes underscores and enforces pure PascalCase.

After step 2, the allowed set is:

```
[a-zA-Z0-9_]
```

This step reduces it to:

```
[a-zA-Z0-9]
```

## Examples

### Valid
- `"MyClass"`
- `"Class123"`

### Invalid
- `"My_Class"` — contains underscore  
- `"_MyClass"` — leading underscore  
- `"MyClass_"` — trailing underscore
```

"""