from typing import Any, TYPE_CHECKING
# Outers
from ......exceptions import SimpleDefinitionError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_type_is_not_empty(
    processed_type: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that '_type' is not an empty container."""

    # 1. Empty container or falsy value
    if not processed_type:
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
            value=processed_type,
            problem=(
                "The '_type' attribute evaluates to an empty value.",
            ),
            expected="A non-empty type, UnionType, or tuple of types.",
            how_to_fix=(
                "Define '_type' as a real type or a non-empty collection of types.",
                "Empty definitions cannot be validated or mapped.",
                "Update '_type' to reflect the actual allowed value structure.",
            ) + acceptable_definitions,
            context=context,
            exception=ValueError,
        )

_DESIGN_NOTES = """
# validate_type_is_not_empty

## Purpose
Prevents `_type` from being defined as an empty container or any falsy value.
Examples of invalid definitions:

- `_type = ()`
- `_type = []`
- `_type = {}`
- `_type = ""`

Empty definitions cannot be validated and provide no structural information.

## Why this validation exists
The type system requires a concrete type matrix.  
If `_type` is empty, downstream logic such as:

- UnionType casting,
- tuple flattening,
- validation,
- instance creation,

cannot operate.

## Pipeline position
This check runs immediately after:

- `validate_type_is_defined`
- `validate_type_is_not_none`

It ensures that `_type` is not missing, not `None`, and not empty.

## Error structure
The helper `_exception_info_for_type` provides:

- class name,
- parent type (constant vs object),
- error name,
- context string,
- example definitions.

These are injected directly into the exception.

## Notes
This validator uses truthiness (`if not processed_type:`) intentionally.
It catches all empty containers without needing explicit type checks.

"""