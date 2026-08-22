from typing import TYPE_CHECKING, NoReturn
# Outers
from .......exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_split_changes_unknown_name(
    instance: "InfrastructureProtocol",
    name: str,
) -> NoReturn:
    """
    Raises an error when a provided update name does not match any constant
    or composite node during the split_changes classification phase.
    """

    # noinspection PyProtectedMember
    raise SimpleRuntimeError(
        error_name="IMMUTABILITY UNKNOWN UPDATE NAME (split_changes)",
        label="update name",
        expected=(
            "A valid constant or composite name defined in the instance metadata."
        ),
        value=repr(name),
        problem=(
            "The provided update name does not match any known constant or composite node.",
            f"Name '{name}' is not part of the instance structure."
        ),
        context=(
            f"Classification attempted on instance '{type(instance).__name__}'.",
            f"Allowed constants: {instance._constant_names_set}",
            f"Allowed composites: {tuple(instance.meta.node_names_set)}",
        ),
        how_to_fix=(
            "Ensure the update name corresponds to an existing constant or composite node.",
            "Check the instance metadata for valid names.",
            "Verify that the name is spelled correctly.",
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_split_changes_unknown_name

## Purpose
Raises a structured error when `split_changes` encounters an update name that
does not correspond to any constant or composite node defined in the instance
metadata.

This validation ensures that mixed updates passed to `with_any` contain only
valid structural keys.

## Why this validation exists
`split_changes` is the first structural step of the mixed‑update pipeline.
Its job is to classify incoming `(name, value)` pairs into:

- constant updates  
- composite updates  

If a name does not belong to either category, the update cannot be processed
safely. Accepting unknown names would lead to:

- inconsistent immutability behavior,  
- silent corruption of update order,  
- unpredictable routing in downstream functions.

Failing early guarantees structural correctness.

## Execution context
Used exclusively inside `split_changes` after tuple validation and before
classification.  
Unlike `process_single_change`, this function does **not** receive the value,
because `split_changes` only performs structural classification.

## What it validates
- The update name must be present in `_constant_names_set`, **or**
- The update name must be present in `meta.node_names_set`.

If neither condition is met, the name is invalid.

## Diagnostic value
The error message provides:
- the invalid name,
- the list of allowed constant names,
- the list of allowed composite names,
- the instance type where the classification failed.

This makes debugging mis‑typed or missing update names trivial.

## Stability guarantee
This validation is part of the immutability subsystem’s structural invariants.
Any change affects:

- routing logic in `with_any`,
- composite recalculation order,
- correctness of immutable updates.

Therefore, the function is intentionally minimal and deterministic.

## Notes
- Pure raise function, no conditional logic.
- Used only by `split_changes`.
- Complements `raise_with_any_unknown_name`, which is used by
  `process_single_change` and includes value diagnostics.
"""