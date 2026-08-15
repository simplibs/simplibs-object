# Outers
from ....exceptions import SimpleDefinitionError
from typing import Any, NoReturn, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...protocols.classes import SimpleClassType


def raise_metadata_is_immutable(
    attr_name: str,
    current_value: Any,
    new_value: Any,
    owner_class: "SimpleClassType"
) -> NoReturn:
    """Raises an error when a metadata field is overwritten."""

    class_name = owner_class.__name__

    raise SimpleDefinitionError(
        error_name="METADATA IMMUTABILITY ERROR",
        label="metadata field",
        value=new_value,
        problem=(
            f"The field '{attr_name}' is already initialized.",
            f"Current value: {repr(current_value)}",
        ),
        expected="Metadata fields are write-once.",
        how_to_fix=(
            "Do not overwrite initialized metadata fields.",
            "Only fields holding UNSET may be assigned.",
            "If you need dynamic state, use a dedicated cache slot.",
        ),
        context=f"Attempted overwrite inside metadata of class '{class_name}'.",
        exception=AttributeError,
    )


_DESIGN_NOTES = """
# raise_metadata_is_immutable

## Purpose
Raises a structured error when code attempts to overwrite a metadata field that
has already been initialized. Metadata fields follow a strict **write‑once**
lifecycle.

## Why this validation exists
Metadata represent the structural identity of a Simple class.  
Once computed, they must remain stable and immutable.  
Allowing overwrites would break determinism and could corrupt the blueprint.

## Execution context
This function is called from `SimpleBaseMetadata.__setattr__` whenever:

- the target field does **not** contain `UNSET`,
- and a new value is being assigned.

It converts a low‑level attribute overwrite into a clear, structured
`SimpleDefinitionError` with actionable guidance.

## Error structure
The raised exception includes:

- the attempted new value,
- the current locked value,
- the attribute name,
- the owning class name,
- instructions on how to fix the issue.

## Notes
If dynamic state is required, use dedicated cache attributes instead of
metadata fields. Metadata must remain immutable for the lifetime of the class.

"""