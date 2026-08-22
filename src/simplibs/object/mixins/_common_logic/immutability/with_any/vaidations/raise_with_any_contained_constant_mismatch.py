from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from ......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_with_any_contained_constant_mismatch(
    instance: "InfrastructureProtocol",
    name: str,
    expected_value: Any,
    actual_value: Any,
) -> NoReturn:
    """
    Raises an error when a contained constant does not match
    the recalculated snapshot value.
    """

    raise SimpleRuntimeError(
        error_name="IMMUTABILITY CONTAINED CONSTANT ERROR",
        label="contained constant mismatch",
        expected=f"Constant '{name}' must match its recalculated value.",
        value=expected_value,
        problem=(
            f"Contained constant '{name}' does not match the recalculated value.",
            f"Provided value: {expected_value!r}",
            f"Recalculated value: {actual_value!r}"
        ),
        context=(
            f"Mixed update attempted on instance '{type(instance).__name__}'.",
            "Contained constants cannot override values derived from composite updates."
        ),
        how_to_fix=(
            "Do not assign values to contained constants directly.",
            "Update the corresponding composite instead.",
            "Contained constants are derived automatically from composite values."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_with_any_contained_constant_mismatch

## Purpose
Raises a structured error when a contained constant provided by the user does
not match the value produced by composite recalculation.

## Why this validation exists
Contained constants lie inside composite branches.  
Their value is determined by the composite update.  
If the user attempts to override such a constant directly, the update becomes
structurally inconsistent.

This check ensures that mixed updates respect composite hierarchy and remain
deterministic.

## Execution context
Used inside `with_any` during step 12.2 after applying all composite updates
and building the intermediate snapshot.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the immutability pipeline.
- Contained constants must always be derived from composite values.
"""