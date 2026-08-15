from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ....exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ...protocols.metadata import SimpleMetaProtocol


def raise_attribut_allready_set(
    cls: "SimpleMetaProtocol",
    attr_name: str,
    new_value: Any,
) -> NoReturn:
    """Raises an error when a class-level attribute is overwritten after initialization."""

    current_value = getattr(cls, attr_name)
    class_name = cls.__name__

    raise SimpleMetadataError(
        error_name="CLASS ATTRIBUTE IMMUTABILITY ERROR",
        label="attribute_already_defined",
        expected="Write-once class-level attributes",
        value=new_value,
        problem=(
            f"Attribute '{attr_name}' on class '{class_name}' is already initialized "
            f"and locked with value: {current_value!r}."
        ),
        context=f"Attempted to overwrite attribute '{attr_name}' on definition class '{class_name}'.",
        how_to_fix=(
            "Class-level blueprint attributes in the Simple system follow a strict 'Write-Once' policy.",
            "Do not modify structural or configuration attributes after they have been initialized.",
            "If dynamic state is required, use instance-level attributes instead of class-level blueprints.",
            "Review the execution path to identify why a second write was attempted.",
        ),
        exception=AttributeError,
    )


_DESIGN_NOTES = """
# raise_attribut_allready_set

## Purpose
Protects declarative blueprint classes from accidental mutation of structural
attributes. Simple metadata fields are write-once and must remain immutable
after initialization to preserve structural integrity.

## Behavior
1. Retrieves the current value of the attribute.
2. Raises `SimpleMetadataError` if a second write is attempted.
3. Provides clear diagnostics and remediation steps.

## Notes
- This function is called exclusively from `SimpleMeta.__setattr__`.
- Prevents corruption of blueprint definitions for constants and composite objects.
- Encourages developers to use instance-level attributes for dynamic behavior.

"""