from typing import Any, TYPE_CHECKING
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_type_tuple_is_not_nested(
    inner_type: Any,
    type_tuple: tuple[Any, ...],
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that a tuple of types is flat."""

    # 1. Nested tuple detected
    if isinstance(inner_type, tuple):
        (
            class_name,
            class_parent,
            error_name,
            context,
            acceptable_definitions,
        ) = _exception_info_for_type(owner_class)

        # 2. Raise structured error
        raise SimpleMetadataError(
            error_name=error_name,
            label="_type",
            value=type_tuple,
            problem=(
                "The '_type' tuple contains a nested tuple.",
            ),
            expected="A flat tuple of types.",
            how_to_fix=(
                "Flatten the tuple into a single sequence.",
                "Nested tuples cannot be processed.",
                "Example: (int, (str, float)) → (int, str, float).",
            ) + acceptable_definitions,
            context=context,
            exception=TypeError,
        )

_DESIGN_NOTES = """
# validate_type_tuple_is_not_nested

## Purpose
Ensures that `_type` defined as a tuple is completely flat.  
Nested tuples cannot be converted into a valid UnionType and would break the
type‑processing pipeline.

## Why this validation exists
The tuple form of `_type` is a legacy syntax:

```
_type = (int, str)
```

It is later converted into:

```
int | str
```

If the tuple contains nested tuples, such as:

```
_type = (int, (str, float))
```

the flattening logic cannot operate.

## Pipeline position
This check runs inside the tuple‑processing branch of `process_type`.  
It is triggered for each element of the tuple.

## Developer experience
Nested tuples often appear due to:

- accidental double‑wrapping,
- copy‑paste errors,
- refactoring mistakes.

The error message includes a clear example of how to flatten the tuple.

## Notes
The validator checks only the current element (`inner_type`).  
The full tuple is included in the error for clarity.
```
"""