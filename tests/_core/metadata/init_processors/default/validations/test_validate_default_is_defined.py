from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_default import _exception_info_for_default
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_default_is_defined(
    default_value: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that '_default' is explicitly defined for a constant."""

    if default_value is UNSET:
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
                "The '_default' attribute is missing.",
            ),
            expected="A concrete default value.",
            how_to_fix=(
                "Define '_default' inside the class body.",
                "Constants must always declare a default value.",
                "If this class is meant to be a composite, define '_inners' instead.",
            ),
            context=context,
            exception=ValueError,
        )



_DESIGN_NOTES = """
# validate_default_is_defined

## Purpose
Ensures that every constant (`SimpleConstant`) declares a `_default` value.  
Constants have no inner structure, so the default value is required to define
their runtime identity.

## Why UNSET is used
`None` is a valid default value.  
`UNSET` is the only reliable marker for “attribute not provided”.

This prevents false positives when a developer intentionally sets:

```
_default = None
```

## Pipeline position
This validation is the first step in `process_default_for_constant`.  
If `_default` is missing, no further checks are executed.

## Developer experience
The error message points the developer toward the correct architectural path:

- If the class is meant to be a constant → define `_default`.
- If the class is meant to be a composite → define `_inners` and `_logic`.

## Notes
This validator is used only for constants.  
Compositions use a separate guard that forbids `_default`.
```
"""