from typing import Any
from simplibs.randomize import RegistryBase
# Outers
from ....exceptions import SimpleLogicError


def validate_registry_is_randomize_registry_base(
    registry: Any
) -> None:
    """Validates that the provided registry argument is None or an instance of RegistryBase.

    Args:
        registry: Candidate registry instance to validate.

    Raises:
        SimpleLogicError: If registry is not None and not a RegistryBase subclass instance.
    """

    if registry is None or isinstance(registry, RegistryBase):
        return

    raise SimpleLogicError(
        error_name="INVALID RANDOMIZE REGISTRY ERROR",
        label="registry",
        expected="None or an instance inheriting from RegistryBase (e.g. LocalRegistry).",
        value=type(registry).__name__,
        problem=(
            "Provided registry parameter is not a valid simplibs-randomize registry instance.",
            "Custom randomizer lookup requires a compatible RegistryBase container."
        ),
        context=(
            f"Received registry argument: {registry!r}",
            f"Received type: '{type(registry).__name__}'",
        ),
        how_to_fix=(
            "Pass None to use default global RANDOMIZERS registry.",
            "Pass a valid LocalRegistry instance created via simplibs.randomize."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_registry_is_randomize_registry_base

## Purpose
Validates that the optional `registry` argument passed to random fillers derives from `simplibs.randomize.RegistryBase`.

## Why this validation exists
The filler resolves randomizers via `registry.randomize(type_hint)`. Invalid objects would fail with attribute errors.
"""