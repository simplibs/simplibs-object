from typing import TYPE_CHECKING, NoReturn, Any
# Outers
from .......exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ......._core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_with_any_unknown_name(
    instance: "InfrastructureProtocol",
    name: str,
    value: Any,
) -> NoReturn:
    """
    Raises an error when a provided update name does not match any constant
    or composite node in the instance.
    """

    # noinspection PyProtectedMember
    raise SimpleMixinError(
        error_name="IMMUTABILITY UNKNOWN UPDATE NAME",
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
            f"Immutable update attempted on instance '{type(instance).__name__}'.",
            f"Provided value: {repr(value)}",
            f"Allowed constants: {instance._constant_names_tuple}",
            f"Allowed composites: {tuple(instance.meta.node_names_set)}",
        ),
        how_to_fix=(
            "Ensure the update name corresponds to an existing constant or composite node.",
            "Check the instance metadata for valid names.",
            "Verify that the name is spelled correctly.",
            "Use `instance.meta.node_names_set` or `instance._constant_names_tuple` to inspect valid keys."
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_with_any_unknown_name

## Purpose
Raises a structured error when `process_single_change` receives a name that is
neither a constant nor a composite node.

## Why this validation exists
The immutability pipeline must reject updates that do not correspond to any
part of the instance structure.  
Accepting unknown names would lead to silent corruption or inconsistent state.

Failing early ensures:
- structural correctness,
- deterministic update behavior,
- clear diagnostics.

## Execution context
Used inside `process_single_change` after validating tuple structure and before
routing to `with_constant` or `with_composite`.

## Notes
- Pure raise function, no conditional logic.
- Used exclusively by the immutability subsystem.
"""