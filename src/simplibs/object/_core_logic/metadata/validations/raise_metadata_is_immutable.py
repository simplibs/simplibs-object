from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ....exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ....protocols.classes import SimpleClassType


def raise_metadata_is_immutable(
    attr_name: str,
    current_value: Any,
    new_value: Any,
    owner_class: "SimpleClassType"
) -> NoReturn:
    """Explicitly raises an error when an already initialized metadata field is attempted to be overwritten."""
    class_name = owner_class.__name__

    raise SimpleMetadataError(
        error_name="METADATA IMMUTABILITY ERROR",
        label="Field already initialized",
        expected="Once initialized, metadata fields are read-only and cannot be overwritten.",
        value=new_value,
        problem=f"The field is already assigned and locked with value: {repr(current_value)}.",
        context=f"Attempted to overwrite attribute '{attr_name}' inside metadata of class '{class_name}'.",
        how_to_fix=(
            "Simple metadata fields are designed to be 'Write-Once'.",
            "After initialization, they become immutable and cannot be altered.",
            "Subsequent overwrites are only permitted for uninitialized slots (holding UNSET).",
            "If dynamic state preservation is required, utilize dedicated cache attributes or properties.",
        ),
        exception=AttributeError
    )


_DESIGN_NOTES = """
# raise_metadata_is_immutable

## Purpose
A specialized exception raiser triggered inside the metadata orchestrator (`SimpleBaseMetadata.__setattr__`) 
when code attempts to mutate an already populated metadata field.

## Execution Context
It enforces the 'Write-Once' paradigm across the lifecycle of class structural properties. 
The function takes the `owner_class` context to reconstruct the absolute path and name 
of the failing blueprint component, mapping the low-level `__setattr__` failure into a high-level 
informative framework message.
"""