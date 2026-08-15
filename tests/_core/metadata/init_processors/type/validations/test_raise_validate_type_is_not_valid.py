from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def raise_validate_type_is_not_valid(
    value_type: Any,
    owner_class: "SimpleClassLike"
) -> NoReturn:
    """Raises an error for completely invalid '_type' definitions."""

    (
        class_name,
        class_parent,
        error_name,
        context,
        acceptable_definitions,
    ) = _exception_info_for_type(owner_class)

    raise SimpleMetadataError(
        error_name=error_name,
        label="_type",
        value=value_type,
        problem=(
            "The '_type' attribute contains an unrecognized value.",
        ),
        expected="A type, UnionType, or flat tuple of types.",
        how_to_fix=(
            "Replace the value with a real type or a tuple of types.",
            "Do not use strings, instances, or nested containers.",
            "Ensure the definition matches the actual value structure.",
        ) + acceptable_definitions,
        context=context,
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_validate_type_is_not_valid

## Purpose
Serves as the final fallback guard in the `process_type` pipeline.  
It is triggered when `_type` does not match **any** supported structural form:

- atomic type (`int`, `str`, `MyClass`)
- modern UnionType (`int | str`)
- flat tuple of types (`(int, str)`)

Anything else is considered invalid.

## Pipeline position
This function is called at the very end of `process_type`.  
All earlier validators have already checked:

- missing `_type`,
- `_type` is None,
- `_type` is empty,
- nested tuples,
- literal None inside tuples,
- NoneType inside UnionType.

If the value still does not match a valid form, control falls through to this
error factory.

## Why this validation exists
Developers sometimes mistakenly assign:

- strings (`"int"`)
- instances (`MyClass()`)
- lists (`[int, str]`)
- dicts (`{"a": 1}`)
- arbitrary objects

These cannot be interpreted as type constraints and would break the metadata
pipeline.

## Diagnostic value
The error includes:

- the invalid value,
- the class name,
- contextual information,
- examples of valid definitions.

This makes debugging straightforward and prevents cryptic runtime failures.

"""