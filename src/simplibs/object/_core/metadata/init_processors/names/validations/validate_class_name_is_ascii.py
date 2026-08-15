# Outers
from ......exceptions import SimpleDefinitionError


def validate_class_name_is_ascii(
    class_name: str
) -> None:
    """Validates that the class name contains only ASCII characters."""

    # 1. Check ASCII constraint
    if class_name.isascii():
        return

    # 2. Raise structured metadata error
    raise SimpleDefinitionError(
        error_name="CLASS NAME NOT ASCII",
        label="class name",
        value=class_name,
        problem=(
            "The name contains non-ASCII characters.",
        ),
        expected="Only basic ASCII characters (A–Z, a–z, 0–9, _).",
        how_to_fix=(
            "Remove accents, hooks, and diacritics.",
            "Convert localized letters to plain ASCII (e.g., 'Měna' → 'Mena').",
            "If the name was created dynamically, verify the input string first.",
        ),
        context="ASCII validation during metadata name processing.",
        exception=ValueError
    )



_DESIGN_NOTES = """
# validate_class_name_is_ascii

## Purpose
Ensures that the class name contains only ASCII characters. This prevents
localized letters, diacritics, and extended Unicode symbols from entering the
metadata naming pipeline.

## Why this validation exists
Python allows Unicode letters inside identifiers.  
Static class definitions rarely contain diacritics, but dynamically generated
classes (`type("Třída", ...)`) often do.

This validator guarantees that all class names remain ASCII-only, which keeps
the naming pipeline predictable and safe.

## What Python already guarantees
Before this check runs, Python ensures:
- the name is always a `str`,
- the name is never empty,
- the name satisfies `isidentifier()` (letters, digits, underscores),
- the name is not a reserved keyword.

Because of this, the only remaining risk is the presence of Unicode letters.

## What this validation enforces
By requiring `isascii()`, the allowed character set becomes:

```
[a-zA-Z0-9_]
```

This excludes:
- diacritics (ě, š, č, ř, í, á, …),
- non-English alphabets (Greek, Cyrillic, Hebrew, …),
- extended Unicode symbols.

## Position in the validation pipeline
This is the second step in the name validation sequence:

1. `validate_class_name_is_identifier`  
   Removes illegal symbols, spaces, hyphens, dots, and leading digits.

2. `validate_class_name_is_ascii`  
   Removes diacritics and non-ASCII characters.

3. `validate_class_name_has_no_underscores`  
   Removes underscores and enforces pure PascalCase.

## Examples

### Valid
- `"MyClass"`
- `"Class123"`
- `"My_Class"`

### Invalid
- `"Třída"` — contains diacritics  
- `"Měsíc"` — contains accented letters  
- `"Ελληνικά"` — Greek alphabet
```
"""