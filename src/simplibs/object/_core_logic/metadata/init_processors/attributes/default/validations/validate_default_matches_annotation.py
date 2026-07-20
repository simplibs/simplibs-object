from typing import Any, TYPE_CHECKING
# Outers
from .......exceptions import SimpleMetadataError
# Inners
from ._exception_info_for_default import _exception_info_for_default
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike


def validate_default_matches_annotation(
    default_value: Any,
    expected_type: Any,
    owner_class: "SimpleClassLike",
) -> None:
    """Validates that the actual '_default' value matches the defined '_type' annotation."""
    # 1. Exception condition
    if not isinstance(default_value, expected_type):

        # 2. Variable resolution
        (class_name,
         class_parent,
         error_name,
         context,
         ) = _exception_info_for_default(owner_class)

        # 3. Exception invocation
        raise SimpleMetadataError(
            error_name=error_name,
            label="Type mismatch for default value",
            expected=f"A value conforming to the defined type: {expected_type}.",
            value=default_value,
            problem="The assigned default value does not match the declared type annotation.",
            context=context,
            how_to_fix=(
                f"Change the '_default' value to strictly match the '{expected_type}' type.",
                "Alternatively, expand or modify the '_type' definition to encompass the current value's type.",
                "For a constant leaf structure (SimpleConstant), a valid, type-compliant '_default' is mandatory.",
            ),
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_default_matches_annotation

## Purpose
This validation bridges the type definition with the actual concrete value. It serves 
as the primary checkpoint for maintaining absolute type safety across the entire 
SimpleObject ecosystem.

## Pre-validation Synergy
Because `validate_type_definition` has already guaranteed that `_type` is formatted 
as a valid structural target for `isinstance()` (handling atomic types, Unions, and 
flat tuples), this component can perform rapid, completely safe type checks without 
worrying about invalid type structures causing native Python errors.

## System Impact
It categorically prevents logical drifts—such as a developer declaring a component 
as an `int` but supplying a `str` as the fallback default. By enforcing this boundary 
during class initialization, it guarantees that runtime `_logic` (or direct default 
access) will never yield an unexpected data type.
"""