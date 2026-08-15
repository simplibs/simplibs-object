from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.classes import SimpleClassLike


def validate_type_is_defined(
    attribute_value: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_type' attribute is explicitly defined."""

    # 1. Missing definition
    if attribute_value is UNSET:
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
            value=attribute_value,
            problem=(
                f"The class '{class_name}' does not define the required '_type' attribute.",
            ),
            expected="A concrete type definition.",
            how_to_fix=(
                f"Define '_type' inside class '{class_name}'.",
                "The type must match the value structure represented by the class.",
            ) + acceptable_definitions,
            context=context,
            exception=AttributeError,
        )



_DESIGN_NOTES = """
# validate_type_is_defined

## Purpose
Ensures that every Simple class explicitly declares its `_type` attribute.
Without this definition, the class cannot participate in the metadata pipeline.

## Why this validation exists
The `_type` attribute is the core schema declaration for both constants and
composite objects. It defines the allowed value structure and is required for:

- validation,
- normalization,
- instance creation,
- static analysis.

If `_type` is missing, the class has no structural identity.

## Sentinel logic
The check uses the `UNSET` sentinel rather than `None` or truthiness.  
This prevents false positives when a user accidentally assigns a falsy value
(e.g., `0`, `False`, `""`) to `_type`.

## Error structure
The helper `_exception_info_for_type` provides:

- class name,
- parent type (constant vs object),
- error name,
- context string,
- example definitions.

These values are injected directly into the exception for clarity.

## Notes
This validation is the first step in `process_type`.  
If `_type` is missing, no further checks are executed.

"""