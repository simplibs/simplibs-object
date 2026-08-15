from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest


# noinspection PyTypeChecker
def assert_mixins_slots_values(
    subtests: Any,
    instance: Any,
    slots_values: Any,
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that specific mixin-provided slots exist on an instance and contain expected values.

    Validates that slot attributes defined by attached mixin classes exist on the runtime object instance
    and hold expected state values. Supports both single key-value tuples and sequences of key-value pairs.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        instance: Runtime object instance under test.
        slots_values: Either a single key-value tuple ``("slot_name", expected_value)``
            or a sequence of tuples ``(("slot_1", val_1), ("slot_2", val_2), ...)``.
        verbose: Enables isolated pytest subtests reporting.
        intro: Optional prefix string added to the generated subtest identity name.
    """
    subintro = "assert_mixins_slots_values::"

    # 1. Normalize input structure
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}normalize_input",
        verbose=verbose,
    ):
        # Single tuple case: ("slot_name", value)
        if isinstance(slots_values, tuple) and len(slots_values) == 2 and isinstance(slots_values[0], str):
            normalized = (slots_values,)
        # Sequence of tuples case: (("slot_1", val_1), ("slot_2", val_2))
        elif isinstance(slots_values, tuple):
            normalized = slots_values
        else:
            pytest.fail(
                f"Parameter 'slots_values' must be a tuple of (name, value) pairs, "
                f"got: {slots_values!r}"
            )

    # 2. Validate structural integrity of each pair
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_pairs",
        verbose=verbose,
    ):
        for pair in normalized:
            if not (isinstance(pair, tuple) and len(pair) == 2):
                pytest.fail(
                    f"Each item in 'slots_values' must be a 2-element tuple of (name, value), "
                    f"got: {pair!r}"
                )

            name, _ = pair
            if not isinstance(name, str):
                pytest.fail(
                    f"Slot name '{name!r}' is not a string identifier. "
                    f"All slot names must be strings."
                )

    # 3. Validate slot attribute presence and state values
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}check_slot_values",
        verbose=verbose,
    ):
        for name, expected_value in normalized:
            if not hasattr(instance, name):
                pytest.fail(
                    f"Instance of class '{instance.__class__.__name__}' "
                    f"does not contain expected slot '{name}'. "
                    f"Available attributes: {dir(instance)}"
                )

            actual_value = getattr(instance, name)

            if actual_value != expected_value:
                pytest.fail(
                    f"Slot '{name}' on instance of '{instance.__class__.__name__}' "
                    f"has unexpected value: expected {expected_value!r}, "
                    f"got {actual_value!r}."
                )


_DESIGN_NOTES = """
# assert_mixins_slots_values (Mixin Slot State Verification Gate)

## Purpose
Verifies that slot attributes defined by attached mixins exist on a runtime instance and hold 
expected initial or calculated values. It acts as a value-level verification step complementing 
structural presence checks.

## Input Flexibility & Normalization Pipeline
1. **Schema Normalization Gate:** Accepts both single pairs `("slot_name", value)` and composite tuples 
   `(("slot_1", val_1), ("slot_2", val_2))` automatically normalizing single-pair inputs into uniform sequences.
2. **Pair Validation:** Ensures every item in the sequence is a 2-element tuple whose first element is a string identifier.
3. **Presence & State Reconciliation:** Iterates over normalized pairs, verifying that `hasattr(instance, slot_name)` 
   evaluates to `True` and that `getattr(instance, slot_name) == expected_value`.

## Pipeline Lifecycle Role
Functions as a specialized state-verification blade within mixin test orchestrators (e.g., `assert_simple_mixin`). 
It ensures that mixins injecting stateful instance variables (`__slots__`) initialize their data members accurately.
"""