# Outers
from ......exceptions import SimpleMetadataError


def validate_class_name_is_ascii(
    class_name: str
) -> None:
    """Validates that the class name contains only standard ASCII characters, prohibiting diacritics."""
    if not class_name.isascii():
        raise SimpleMetadataError(
            error_name="CLASS NAME NOT ASCII",
            label="Non-standard characters detected",
            value=class_name,
            problem="The class name contains disallowed characters (localized diacritics or non-ASCII symbols).",
            expected="Strictly basic ASCII characters (A-Z, a-z, 0-9, _).",
            how_to_fix=(
                "The class possesses an invalid name — it was likely generated dynamically with an invalid input string.",
                "Remove all accents, hooks, and diacritics from the class identifier (e.g., transform 'Měna' to 'Mena').",
                "Review the runtime blueprint definition layer or contact the system administrator.",
            ),
            context="Structural validation of dynamic class identifiers during metadata extraction.",
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_class_name_is_ascii

## Purpose
Validates that the class name of a Simple structure contains only ASCII characters without any localized diacritics. It is designed to evaluate names extracted directly from live class objects (`ClassName.__name__`). This check operates with the guarantees established by the upstream Python parser or preceding validation steps.

## What Python/Upstream Already Guarantees (Standard Class Context)
When a class is evaluated here, we safely operate under the assumption that the string has already been parsed as a structural entity. This means we do not need to repeat checks for the following:
1. **Type is strictly str** — `ClassName.__name__` always returns a primitive string.
2. **Never empty** — Python never permits empty class identifiers (`class :` is a syntax error).
3. **Valid Identifier Pattern** — The value structurally satisfies `isidentifier()`, meaning it contains only letters, digits, and underscores, does not start with a digit, and contains no spaces or punctuation.
4. **Not a keyword** — Python natively rejects reserved keywords (`class class:` is a syntax error).

Because of these pre-conditions, the class name string contains nothing but `[a-zA-Z0-9_]` alongside valid Unicode word characters (like localized letters).

## What This Validation Enforces
By checking `isascii()`, we shrink the allowed character space to guarantee:
- ✓ Only characters belonging to the standard ASCII table (0-127).
- ✓ Absolute exclusion of diacritics, accents, hooks, or non-English letters.
- ✓ Absolute exclusion of any extended Unicode symbols.

**Practical Output:** If a string satisfies both `isidentifier()` and this `isascii()` check, it is guaranteed to consist exclusively of:

```

[a-zA-Z0-9_]

```

## Validation Pipeline Architecture
This validation represents the second pillar of the structural name screening process:
1. `validate_class_name_is_identifier`: Filters out illegal symbols, spaces, hyphens, and starting digits.
2. `validate_class_name_is_ascii` (This function): Strips out diacritics and non-ASCII localized alphabets.
3. `validate_class_name_has_no_underscores`: Strips out underscores, finalizing a pure PascalCase requirement `[a-zA-Z0-9]`.

## Examples
```python
# VALID (Passes this check; underscores are handled downstream)
validate_class_name_is_ascii("MyClass")               # OK
validate_class_name_is_ascii("Class123")              # OK
validate_class_name_is_ascii("My_Class")              # OK

# INVALID (Raises SimpleMetadataError via ValueError)
validate_class_name_is_ascii("Třída")                 # Fail: contains a hook 'ř' and accent 'í'
validate_class_name_is_ascii("Mesíc")                 # Fail: contains an accent 'í'
validate_class_name_is_ascii("Ελληνικά")              # Fail: Greek alphabet

```

"""