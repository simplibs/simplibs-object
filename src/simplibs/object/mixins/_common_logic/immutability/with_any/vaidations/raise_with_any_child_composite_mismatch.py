from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from ......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_with_any_child_composite_mismatch(
    instance: "InfrastructureProtocol",
    name: str,
    expected_value: Any,
    actual_value: Any,
) -> NoReturn:
    """
    Raises an error when a child composite value does not match
    the recalculated snapshot value.
    """

    raise SimpleRuntimeError(
        error_name="IMMUTABILITY CHILD COMPOSITE ERROR",
        label="child composite mismatch",
        expected=f"Child composite '{name}' must match its recalculated value.",
        value=expected_value,
        problem=(
            f"Child composite '{name}' does not match the recalculated value.",
            f"Provided value: {expected_value!r}",
            f"Recalculated value: {actual_value!r}"
        ),
        context=(
            f"Mixed update attempted on instance '{type(instance).__name__}'.",
            "Child composites cannot be directly overridden when they depend on parent composites."
        ),
        how_to_fix=(
            "Do not assign values to child composites directly.",
            "Update the corresponding root composite instead.",
            "Child composite values are derived automatically from parent composites."
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_with_any_child_composite_mismatch

## Purpose
Raises a structured error when a child composite value provided by the user
does not match the value produced by recalculating parent composites.

## Why this validation exists
Child composites are **derived values**.  
Their value depends on the decomposition of higher-level composites.  
If the user attempts to override a child composite directly, the update becomes
structurally inconsistent.

This check ensures that mixed updates remain deterministic and that composite
hierarchies are respected.

## Execution context
Used inside `with_any` after applying all root composites and building the
intermediate snapshot.  
It validates that child composites match their recalculated values.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the immutability pipeline.
- Child composites must always be derived from parent composites.
"""