from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_type_is_defined(
    attribute_value: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the required '_type' attribute is explicitly defined on the class."""

    # 1. Exception condition
    if attribute_value is UNSET:

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
            label="Attribute '_type' is missing",
            expected="The class must explicitly declare its target data type to guarantee data integrity.",
            problem=f"The class '{class_name}' completely lacks the mandatory '_type' attribute definition.",
            context=context,
            how_to_fix=(
                f"Define the '_type' attribute directly within the body of class '{class_name}'.",
                "The defined type must accurately reflect the value structure that this class represents.",
            ) + acceptable_definitions,
            exception=AttributeError
        )


_DESIGN_NOTES = """
# validate_type_is_defined

## Purpose
Ensures absolute structural integrity by guaranteeing that no data object class 
definition enters the system without an explicitly declared type boundary constraint.

## Integration & Sentinel Logic
This guard is executed at the very front of the validation logic within `process_type`. 
By passing `getattr(owner_class, "_type", UNSET)` down to this function, it checks 
for reference absence using a dedicated `UNSET` singleton rather than a truthiness 
or `None` check, protecting against cases where a user might accidentally assign 
falsy values to the attribute.

## Architectural Enforcement
Unlike native Python where attributes are completely fluid, this object metadata 
framework treats type definitions as hard schema declarations. Raising an `AttributeError` 
wrapped into a domain-specific `SimpleMetadataError` ensures compile-time level 
rejection during metaclass or descriptor initialization.
"""