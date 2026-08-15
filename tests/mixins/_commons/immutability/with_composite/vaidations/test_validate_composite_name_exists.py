from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def validate_composite_name_exists(
    instance: "InfrastructureProtocol",
    name: str,
) -> None:
    """
    Validates that the provided name refers to an existing composite node.
    """

    if name in instance.meta.node_names_set:
        return

    raise SimpleMixinError(
        error_name="IMMUTABILITY COMPOSITE UPDATE ERROR",
        label="composite name",
        expected="Name must refer to a valid composite node.",
        value=name,
        problem=(
            f"Composite '{name}' does not exist in the instance metadata.",
            "Immutable composite update cannot be applied."
        ),
        context=(
            f"Composite update attempted on instance '{type(instance).__name__}'.",
            f"Valid composite names: {tuple(instance.meta.node_names_set)}"
        ),
        how_to_fix=(
            "Ensure that the provided name refers to a composite node.",
            "Check the instance metadata for available composite names.",
            "If the name refers to a constant, use with_constant instead."
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# validate_composite_name_exists

## Purpose
Ensures that composite updates target an existing node.  
Composite names must be present in `meta.node_names_set`, otherwise the update
cannot be routed through decomposition and owner recalculation.

## Why this validation exists
Composite updates rely on metadata paths, decomposition rules, and owner
hierarchies.  
If the name does not exist:

- the pipeline cannot locate the node,
- decomposition cannot run,
- owner propagation becomes undefined,
- snapshot reconstruction would be inconsistent.

Failing early prevents structural corruption.

## Execution context
This validation is used inside `with_composite` before any decomposition or
snapshot manipulation occurs.  
It is the first structural check for composite updates.

## Notes
- Pure validation function, no additional logic.
- Used exclusively by the immutability pipeline.
- Composite names must be defined in metadata.
"""