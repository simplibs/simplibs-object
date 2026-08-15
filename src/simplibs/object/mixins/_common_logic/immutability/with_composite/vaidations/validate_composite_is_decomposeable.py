from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def validate_composite_is_decomposeable(
    instance: "InfrastructureProtocol",
    name: str,
) -> None:
    """
    Validates that the composite node supports decomposition.
    """

    if instance.meta.is_decomposeable:
        return

    raise SimpleLogicError(
        error_name="IMMUTABILITY COMPOSITE UPDATE ERROR",
        label="composite decomposability",
        expected="Composite nodes must support decomposition.",
        value=name,
        problem=(
            f"Composite '{name}' is not decomposable.",
            "Inner values cannot be recalculated for this node."
        ),
        context=(
            f"Composite update attempted on instance '{type(instance).__name__}'.",
            "The instance metadata reports that decomposition is disabled."
        ),
        how_to_fix=(
            "Enable decomposition for this composite node in its metadata.",
            "If the node is meant to be constant, use with_constant instead.",
            "If decomposition is intentionally disabled, do not update this node as a composite."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_composite_is_decomposeable

## Purpose
Ensures that composite updates are only applied to nodes that support
decomposition.  
Composite updates require inner-node recalculation, which is impossible when
`meta.is_decomposeable` is False.

## Why this validation exists
Decomposition is the mechanism that propagates composite values into their
inner nodes.  
If decomposition is disabled:

- inner recalculation cannot run,
- owner propagation becomes inconsistent,
- the composite update would produce an invalid snapshot.

Failing early prevents structural corruption.

## Execution context
This validation is used inside `with_composite` immediately after verifying
that the composite name exists.  
It is the second structural check before any snapshot manipulation occurs.

## Notes
- Pure validation function, no additional logic.
- Used exclusively by the immutability pipeline.
- Composite nodes must explicitly support decomposition.
"""