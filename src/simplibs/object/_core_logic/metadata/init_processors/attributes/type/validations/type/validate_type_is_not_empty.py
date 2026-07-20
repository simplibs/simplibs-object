from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_type_is_not_empty(
    processed_type: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_type' attribute is not defined as an empty container or collection."""

    # 1. Exception condition
    if not processed_type:

        # 2. Variable resolution
        (class_name,
         class_parent,
         error_name,
         context,
         acceptable_definitions
         ) = _exception_info_for_type(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Empty definition is not allowed",
            value=processed_type,
            expected="A non-empty type, UnionType, or a tuple containing valid types.",
            problem="The class attribute '_type' must not be evaluated as an empty object or container.",
            context=context,
            how_to_fix=(
                "The class type must accurately reflect the value structure that this class represents.",
                "The type definition cannot be empty, as downstream validators require concrete type definitions.",
                "Change the '_type' attribute to target the actual class or types allowed for this object.",
            ) + acceptable_definitions,
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_type_is_not_empty

## Purpose
Prevents developers from initializing object metadata with empty collections or empty 
falsy values (such as an empty tuple `_type = ()`), which would bypass type checking 
mechanisms completely.

## Pipeline Integration & Truthiness Catch
This validator is triggered early in the `process_type` flow. Because it checks for 
general truthiness via `if not processed_type:`, it works in tandem with the previous 
`UNSET` checks. It specifically catches initialized but empty structural constructs 
that evaluate to `False` in a boolean context.

## Architectural Enforcement
Downstream casting, instance comparisons, and data mapping functions rely entirely 
on a populated type matrix. An empty type constraint would break runtime execution 
during validation loops; by shifting the error to the initialization phase with 
a clear `ValueError`, debugging remains straightforward.
"""