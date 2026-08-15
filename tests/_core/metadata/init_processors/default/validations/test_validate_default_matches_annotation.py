from typing import Any, TYPE_CHECKING
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_default import _exception_info_for_default
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_default_matches_annotation(
    default_value: Any,
    expected_type: Any,
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that '_default' matches the declared '_type'."""

    if not isinstance(default_value, expected_type):
        (
            class_name,
            class_parent,
            error_name,
            context,
        ) = _exception_info_for_default(owner_class)

        raise SimpleMetadataError(
            error_name=error_name,
            label="_default",
            value=default_value,
            problem=(
                "The default value does not match the declared type.",
            ),
            expected=f"A value of type {expected_type}.",
            how_to_fix=(
                f"Change '_default' to match {expected_type}.",
                "Or update '_type' to include the value's type.",
                "Constants require a type‑compliant default value.",
            ),
            context=context,
            exception=TypeError,
        )



_DESIGN_NOTES = """
# validate_default_matches_annotation

## Purpose
Ensures that the `_default` value matches the type declared in `_type`.  
This is the core rule for constant leaf nodes: the default value defines the
runtime identity of the constant and must be type‑safe.

## Why this validation exists
The type system guarantees that:

- `_type` is valid,
- `_type` is safe for `isinstance`,
- `_type` is normalized (atomic, UnionType, or tuple → UnionType).

Because of this, the validator can rely on a simple `isinstance` check.

Examples of invalid definitions:

```
_type = int
_default = "hello"     # invalid
```

```
_type = int | str
_default = 3.14        # invalid
```

## Pipeline position
This validation runs after:

- `_default` is confirmed to exist,
- `_type` is fully validated and normalized.

If the type does not match, initialization stops immediately.

## Developer experience
The error message clearly explains:

- what type was expected,
- what value was provided,
- how to fix the mismatch.

## Notes
This validator is used only for constants.  
Compositions do not allow `_default` at all.
```
"""