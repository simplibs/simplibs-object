from typing import Any
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing import maybe_subtest
# Outers
from ...tools.InnerValue import InnerValue


def assert_value_change(
    subtests: Any,
    instance: Any,
    *,
    value: Any | InnerValue,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """
    Universal value-change assertion.

    - Accepts Any or InnerValue
    - Resolves target instance (main or inner)
    - Validates new value
    - Ensures value differs from default and original
    - Applies value via setter
    - Ensures value actually changed

    Returns:
        new_value
    """

    subintro = "assert_value_change::"

    # 1. Resolve target instance + value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}resolve_target",
        verbose=verbose,
    ):
        if isinstance(value, InnerValue):
            target, value = value.as_instance_tuple(instance)
            if target is UNSET:
                pytest.fail("InnerValue path could not be resolved.")
        else:
            target = instance
            new_value = value

    # 2. Validate new value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_new_value",
        verbose=verbose,
    ):
        if not target.validate(value, return_bool=True):
            pytest.fail(f"Value '{value}' is not valid for '{target.meta.name_snake}'.")

    # 3. Ensure new value differs from original
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}not_original",
        verbose=verbose,
    ):
        if new_value == target.value:
            pytest.fail(
                f"New value must differ from original value ({old_value})."
            )

    # 4. Apply new value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_value",
        verbose=verbose,
    ):
        try:
            target.value = new_value
        except Exception as exc:
            pytest.fail(f"Failed to apply new value: {exc}")

    # 5. Ensure value actually changed
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}value_changed",
        verbose=verbose,
    ):
        if target.value != new_value:
            pytest.fail(
                f"Value did not change: expected {value}, got {target.value}"
            )

    return new_value
