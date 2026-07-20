from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exception_info_for_type import _exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def raise_validate_type_is_not_valid(
    value_type: Any,
    owner_class: "SimpleClassLike"
) -> NoReturn:
    """Raises an exception indicating that the provided '_type' attribute is completely unrecognized or invalid."""

    # 1. Variable resolution
    (class_name,
     class_parent,
     error_name,
     context,
     acceptable_definitions
     ) = _exception_info_for_type(owner_class)

    # 2. Exception invocation
    raise SimpleMetadataError(
        error_name=error_name,
        label="Invalid type definition value",
        value=value_type,
        expected="A valid type, UnionType, or flat tuple of types.",
        problem=f"The class attribute '_type' contains an unrecognized value that cannot be interpreted as a valid type constraint.",
        context=context,
        how_to_fix=(
            "Modify the '_type' attribute so that it contains a valid structural type definition.",
            "The defined type must accurately reflect the actual concrete instances the class represents.",
            "Ensure you are not passing a string representation, instance data, or complex nested containers.",
        ) + acceptable_definitions,
        exception=TypeError
    )


_DESIGN_NOTES = """
# raise_validate_type_is_not_valid

## Purpose
Acts as the final generic fallback guard (the "catch-all") within the `process_type` 
orchestration workflow. If a user provides an attribute definition that completely 
evades all structured parsing paths, this function halts initialization.

## Pipeline Integration & Strategy
This block is intentionally decoupled from an active conditional statement because 
it is invoked natively at the very end of the `process_type` evaluation sequence. 
If `_type` is neither an atomic `type`, a modern `UnionType`, nor a Python `tuple`, 
control falls through directly into this exception factory.

## Diagnostic Value
By printing out the exact structural blueprint from `_exception_info_for_type`, the 
framework instantly shows developers what forms are acceptable, correcting attempts 
to use unsupported meta-expressions or literal instances as type annotations.
"""