# Outers
from ......exceptions import SimpleMetadataError


def validate_class_name_has_no_underscores(
    class_name: str
) -> None:
    """Validates that the class name does not contain any underscores (_), enforcing a pure alphanumeric pattern."""
    if "_" in class_name:
        raise SimpleMetadataError(
            error_name="CLASS NAME CONTAINS UNDERSCORE",
            label="Invalid character in name",
            value=class_name,
            problem="The class name contains an underscore (_), which is strictly prohibited within the SimpleObject architecture.",
            expected="Exclusively alphanumeric characters (A-Z, a-z, 0-9).",
            how_to_fix=(
                "Remove all underscores from the class name string.",
                "Example: Convert 'My_Class' to 'MyClass' (adhere strictly to PascalCase convention).",
                "Underscores are reserved for the framework's internal metadata derivation layers and generated identifiers.",
            ),
            context="Structural validation of dynamic class identifiers during metadata extraction.",
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_class_name_has_no_underscores

## Purpose
A complementary validation step ensuring that no underscore character (_) is present within the name of a SimpleObject subclass. This rule is designed to be executed **after** passing the `validate_class_name_is_ascii` check. 

The SimpleObject ecosystem explicitly bans underscores in public class identifiers because:
- Underscores are structurally reserved for framework internals and private low-level processing.
- Class names are used to auto-derive other operational entity markers and internal attributes.
- Allowing user-defined underscores could lead to prefix/suffix collisions with system-generated tokens.

## Relation to the Validation Pipeline
Once a class name successfully passes `validate_class_name_is_ascii`, the permitted character subset is guaranteed to be exactly:

```

[a-zA-Z0-9_]

```
This subsequent check **further restricts** that set to a pure alphanumeric blueprint:

```

[a-zA-Z0-9]

```
Because all other punctuation, spaces, and diacritics were dropped in preceding steps, checking for the literal underscore token is the only task remaining to guarantee a clean PascalCase identifier.

## Separation of Concerns
Splitting this architectural filter into an isolated component offers clean engineering advantages:
- `validate_class_name_is_ascii`: Addresses standard localized/diacritic semantics (global compliance).
- `validate_class_name_has_no_underscores` (This function): Addresses strict framework architectural conventions (SimpleObject compliance).

Each operation focuses on a single responsibility, maximizing maintainability and test mapping precision.

## Examples
```python
# VALID (Contains no underscores)
validate_class_name_has_no_underscores("MyClass")         # OK
validate_class_name_has_no_underscores("Class123")        # OK

# INVALID (Raises SimpleMetadataError via ValueError)
validate_class_name_has_no_underscores("My_Class")        # Fail: internal underscore
validate_class_name_has_no_underscores("_MyClass")        # Fail: leading underscore
validate_class_name_has_no_underscores("MyClass_")        # Fail: trailing underscore

```

"""