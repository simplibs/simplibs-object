from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest


def assert_mixins_slots_values(
    subtests: Any,
    instance: Any,
    slots_values: Any,
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Validates that specific mixin-provided slots exist on the instance
    and contain expected values.

    Expected input formats:
        - (("slot_name", expected_value), ("slot2", expected_value2), ...)
        - ("slot_name", expected_value)   # single pair
    """

    subintro = "assert_mixins_slots_values::"

    # ------------------------------------------------------------
    # 1) Normalize input
    # ------------------------------------------------------------
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}normalize_input",
        verbose=verbose,
    ):
        # Single tuple case: ("slot_name", value)
        if isinstance(slots_values, tuple) and len(slots_values) == 2 and isinstance(slots_values[0], str):
            normalized = (slots_values,)
        # Multi-tuple case: (("slot", value), ("slot2", value2))
        elif isinstance(slots_values, tuple):
            normalized = slots_values
        else:
            pytest.fail(
                f"Parameter 'slots_values' must be a tuple of (name, value) pairs, "
                f"got: {slots_values!r}"
            )

    # ------------------------------------------------------------
    # 2) Validate structure of each pair
    # ------------------------------------------------------------
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_pairs",
        verbose=verbose,
    ):
        for pair in normalized:
            if not (isinstance(pair, tuple) and len(pair) == 2):
                pytest.fail(
                    f"Each item in 'slots_values' must be a tuple of (name, value), "
                    f"got: {pair!r}"
                )

            name, _ = pair
            if not isinstance(name, str):
                pytest.fail(
                    f"Slot name '{name!r}' is not a string. "
                    f"All slot names must be strings."
                )

    # ------------------------------------------------------------
    # 3) Validate slot presence and value
    # ------------------------------------------------------------
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
                    f"Slot '{name}' on instance '{instance.__class__.__name__}' "
                    f"has unexpected value: expected {expected_value!r}, "
                    f"got {actual_value!r}."
                )
