from typing import Any, TYPE_CHECKING
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_type_from_tuple_is_not_none(
    inner_type: Any,
    type_tuple: tuple[Any, ...],
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that a tuple element is not literal None."""

    # 1. Literal None detected
    if inner_type is None:
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
                "The '_type' tuple contains a literal None value.",
            ),
            expected="A real type or class reference.",
            how_to_fix=(
                "Replace literal None with a real type.",
                "If absence of value is intended, use NoneType instead.",
                "Literal None cannot be part of a type tuple.",
            ) + acceptable_definitions,
            context=context,
            exception=TypeError,
        )


_DESIGN_NOTES = """
# validate_type_from_tuple_is_not_none

## Purpose
Prevents developers from placing literal `None` inside a tuple of types, such as:

```
_type = (int, None)
```

Literal `None` is not a type and cannot be used with `isinstance`.

## Why this validation exists
The tuple form of `_type` is later converted into a UnionType.  
If the tuple contains literal `None`, the conversion would produce an invalid
UnionType and break the type system.

Correct form:

```
_type = (int, NoneType)
```

Incorrect form:

```
_type = (int, None)
```

## Pipeline position
This check runs inside the tuple‑processing branch of `process_type`.  
It is triggered for each element of the tuple.

## Developer experience
Literal `None` often appears due to:

- misunderstanding the difference between `None` and `NoneType`,
- copy‑paste errors,
- attempts to express optionality inside `_type`.

The error message explains the correct approach.

## Notes
Optionality must be modeled at a higher level.  
The core type registry must contain only real types.
```

"""