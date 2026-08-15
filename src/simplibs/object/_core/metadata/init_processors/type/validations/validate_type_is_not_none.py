from typing import Any, TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_type_is_not_none(
    value_type: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that '_type' is not set to literal None."""

    # 1. Literal None is invalid
    if value_type is None:
        (
            class_name,
            class_parent,
            error_name,
            context,
            acceptable_definitions,
        ) = _exception_info_for_type(owner_class)

        # 2. Raise structured error
        raise SimpleDefinitionError(
            error_name=error_name,
            label="_type",
            value=value_type,
            problem=(
                "The '_type' attribute is set to literal None.",
            ),
            expected="A concrete type or a UnionType.",
            how_to_fix=(
                "Replace literal None with a real type.",
                "If you intended to allow absence of value, use NoneType instead.",
                "Literal None cannot serve as a structural type definition.",
            ) + acceptable_definitions,
            context=context,
            exception=TypeError,
        )



_DESIGN_NOTES = """
# validate_type_is_not_none

## Purpose
Prevents developers from assigning literal `None` to the `_type` attribute.
Literal `None` cannot represent a structural type and would break validation,
normalization, and instance creation.

## Why this validation exists
The `_type` attribute must always point to:

- a concrete Python type (e.g., `int`, `str`, `MyClass`),
- a UnionType (e.g., `int | str`),
- or a tuple of types (later converted to a UnionType).

Literal `None` is not a type and cannot be used with `isinstance`.

## Pipeline position
This check runs immediately after:

- `validate_type_is_defined`
- and before deeper structural checks.

It ensures that `_type` is not missing and not `None`.

## Error structure
The helper `_exception_info_for_type` provides contextual data:

- class name,
- parent type (constant vs object),
- error name,
- context string,
- example definitions.

These are injected directly into the exception.

## Notes
If the developer wants to allow `None` as a valid value, they must use
`NoneType` from the `types` module, not literal `None`.

"""