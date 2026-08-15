from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ...tools.InnerValue import InnerValue
from ..base.assert_value_change import assert_value_change
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleInstanceLike


def assert_reactivity_upward(
    subtests: Any,
    instance: "SimpleInstanceLike",
    *,
    new_value: InnerValue,
    verbose: bool = True,
    verbose_value_change: bool = True,
    intro: str = "",
) -> None:
    """
    Verifies upward reactivity of composite instances:
    - inner value change must update composite value
    """

    subintro = "test_reactivity_upward::"

    # 1) Capture original composite value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}capture_original_composite",
        verbose=verbose,
    ):
        original_composite_value = instance.value

    # 2) new_value MUST be InnerValue
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}validate_input_type",
        verbose=verbose,
    ):
        if not isinstance(new_value, InnerValue):
            pytest.fail(
                "Upward reactivity requires InnerValue, direct value cannot be used."
            )

    # 3) Apply inner value change (validation + setter handled inside)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_inner_value",
        verbose=verbose,
    ):
        assert_value_change(
            subtests,
            instance,
            value=new_value,
            verbose=verbose_value_change and verbose,
            intro=intro,
        )

    # 4) Composite value MUST change
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}composite_changed",
        verbose=verbose,
    ):
        if instance.value == original_composite_value:
            pytest.fail(
                "Composite value did not change after inner update — "
                "upward reactivity is broken."
            )
