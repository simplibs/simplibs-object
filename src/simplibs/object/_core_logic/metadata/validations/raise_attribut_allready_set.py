from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ....exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ....protocols.metadata import SimpleMetaProtocol


def raise_attribut_allready_set(
    cls: "SimpleMetaProtocol",
    attr_name: str,
    new_value: Any
) -> NoReturn:
    """Explicitly raises an error when an already defined class-level attribute is attempted to be modified."""
    class_name = cls.__name__
    current_value = getattr(cls, attr_name)

    raise SimpleMetadataError(
        error_name="CLASS ATTRIBUTE IMMUTABILITY ERROR",
        label="Attribute already defined",
        expected="Once defined, class-level attributes of Simple structures are immutable and cannot be altered.",
        value=new_value,
        problem=f"The attribute '{attr_name}' is already assigned on the class and locked with value: {repr(current_value)}.",
        context=f"Attempted to mutate attribute '{attr_name}' on the definition class '{class_name}'.",
        how_to_fix=(
            "Simple system blueprint classes protect their definition definitions via 'Write-Once' constraints.",
            "Modifying already initialized structural attributes or configuration parameters at runtime is strictly disallowed.",
            "Review the runtime execution path to locate why a class-level attribute override was triggered.",
            "If dynamic, stateful instance logic is required, manipulate instance-level attributes rather than class-level blueprints.",
        ),
        exception=AttributeError
    )


_DESIGN_NOTES = """
# raise_attribut_allready_set

## Purpose
A specialized exception raiser triggered inside the system's metaclass (`SimpleMeta.__setattr__`) 
when code attempts to modify or overwrite an already populated class-level property on a declarative blueprint.

## Execution Context
It acts as the first line of defense protecting the integrity of defined `SimpleConstant` or `SimpleObject` 
blueprints. It prevents downstream structural corruption by blocking subsequent writes to key fields or hooks. 
It uses the class type reference (`cls`) to safely extract the current state for high-quality problem reporting.
"""