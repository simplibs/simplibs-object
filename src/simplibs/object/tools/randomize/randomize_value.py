from typing import TYPE_CHECKING
from simplibs.randomize import randomize, RandomizeError
from simplibs.randomize.registry import RegistryBase
# Inners
from ._validations import (
    validate_instance_is_simple_constant_base,
    validate_retries_is_int,
    validate_retries_is_greater_than_zero,
    validate_registry_is_randomize_registry_base,
    validate_skip_unregistered_is_bool,
    raise_random_data_filler_exhausted,
)
# Outers
from ...SimpleConstant import SimpleConstant
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.instance import SimpleInstanceLike


def randomize_value(
    instance: "SimpleInstanceLike",
    *,
    retries: int,
    registry: RegistryBase | None,
    skip_unregistered: bool = False,
    validate: bool = True,
) -> "SimpleInstanceLike":
    """Generates and assigns a random valid value to a single target leaf instance.

    Attempts up to ``retries`` times to generate a distinct value matching the target type hint via
    ``simplibs-randomize``. If setter assignment succeeds without validation errors, returns the mutated instance.

    Args:
        instance: Target ``SimpleConstant`` or leaf instance to randomize.
        retries: Maximum number of generation and assignment attempts.
        registry: Optional custom ``RegistryBase`` instance providing isolated type randomizers.
        skip_unregistered: If ``True``, ignores unregistered types rather than raising ``RandomizeError``.
        validate: Enables argument type and boundary validation when ``True``.

    Returns:
        The mutated instance carrying a new valid value.

    Raises:
        SimpleLogicError: If parameter validation fails or retry attempts are exhausted.
        RandomizeError: If the target value type hint is unregistered and ``skip_unregistered`` is ``False``.
    """

    # ------------------------------------------------------------
    # 1. Parameter Validation Gate
    # ------------------------------------------------------------
    if validate and not (
        isinstance(instance, SimpleConstant)
        and isinstance(retries, int) and retries > 0
        and (registry is None or isinstance(registry, RegistryBase))
        and isinstance(skip_unregistered, bool)
    ):
        validate_instance_is_simple_constant_base(instance)
        validate_retries_is_int(retries)
        validate_retries_is_greater_than_zero(retries)
        validate_registry_is_randomize_registry_base(registry)
        validate_skip_unregistered_is_bool(skip_unregistered)

    # ------------------------------------------------------------
    # 2. Randomizer Lookup Resolution
    # ------------------------------------------------------------
    value_randomizer = registry.randomize if registry else randomize

    # ------------------------------------------------------------
    # 3. Random Generation & Assignment Loop
    # ------------------------------------------------------------
    instance: "SimpleInstanceLike"
    for _ in range(retries):

        # 3.1 Generate candidate value matching type hint
        try:
            value_type = instance.meta.value_type
            new_value = value_randomizer(value_type)
        except RandomizeError:
            if skip_unregistered:
                return instance
            raise

        # 3.2 Ensure candidate value differs from current state
        if new_value == instance.value:
            continue

        # 3.3 Attempt state mutation via property setter
        # noinspection PyBroadException
        try:
            instance.value = new_value
            return instance

        # 3.4 Catch setter validation failures and retry
        except Exception:
            continue

    # ------------------------------------------------------------
    # 4. Exhaustion Safeguard
    # ------------------------------------------------------------
    raise_random_data_filler_exhausted(instance, retries)


_DESIGN_NOTES = """
# randomize_value (Single Leaf Randomization Engine)

## Purpose
Acts as the low-level value generation and assignment engine for individual leaf nodes (`SimpleConstant`). 
It bridges the framework's instance state setters with the `simplibs-randomize` engine.

## Execution Safeguards
1. **Validation Fast Path:** Executes parameter validation functions with exact positional inputs when `validate=True`.
2. **Registry Scoping:** Resolves `registry.randomize` when a local registry is provided; otherwise falls back 
   to global `randomize`.
3. **Setter Retry Loop:** 
   - Generates candidate value based on `instance.meta.value_type`.
   - Rejects identical values to guarantee state mutation (`new_value == instance.value`).
   - Traps setter validation failures (`try ... except Exception`) to attempt generating alternative valid values up to `retries` limit.
4. **Exhaustion Exception:** If no valid distinct value is set within `retries` count, invokes `raise_random_data_filler_exhausted`.

## Framework Usage Locations
1. **`random_data_filler.py`:** Invoked on constant leaves and decomposable composites during tree traversal.
"""