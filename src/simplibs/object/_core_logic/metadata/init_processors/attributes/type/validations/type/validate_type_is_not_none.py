from typing import Any, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_type_is_not_none(
    value_type: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """Validates that the '_type' attribute is not explicitly set to a literal 'None' value."""

    # 1. Exception condition
    if value_type is None:

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
            label="Literal 'None' detected as type definition",
            expected="A valid type or class reference representing the output object.",
            problem=f"The class attribute '_type' is explicitly set to a literal 'None' value.",
            context=context,
            how_to_fix=(
                "Modify the '_type' attribute so that it does not contain the literal value 'None'.",
                "The defined type must accurately reflect the value structure that this class represents.",
                "If you intended to allow absence of value, use 'NoneType' from the 'types' module instead of 'None'.",
                "Note that representing 'None' as a core value type is architecturally disallowed in this framework.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_type_is_not_none

## Purpose
Prevents developers from assigning a literal `None` directly to the `_type` metadata 
attribute, ensuring that the target object will always map to a real, evaluable type.

## Pipeline Integration
This guard runs alongside `validate_type_is_defined` and `validate_type_is_not_empty` 
at the very entrance of the `process_type` pipeline. It explicitly intercepts values 
where the attribute exists but evaluates directly to the `None` singleton before 
any structural type mapping or tuple flattening takes place.

## Architectural Reasoning
In standard Python, `isinstance(val, None)` throws a native, generic `TypeError`. 
By catching this invalid type declaration at compile/initialization time, the 
framework shields the user from late runtime errors and explicitly instructs them 
to use proper structural definitions or `NoneType` if applicable.
"""