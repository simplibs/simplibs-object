from typing import Any
import pytest
from simplibs.exception.testing import maybe_subtest
# Outers
from ..base.assert_value_change import assert_value_change


def assert_reactivity_downward(
    subtests: Any,
    instance: Any,
    *,
    new_value: Any,
    verbose: bool = True,
    verbose_value_change: bool = True,
    intro: str = "",
) -> None:
    """
    Verifies downward reactivity of composite instances:
    - composite value change must update all inner values
    """

    subintro = "test_reactivity_downward::"
    meta = instance.meta

    # 1) Composite must be a non-constant object
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}is_composite",
        verbose=verbose,
    ):
        if meta.is_constant:
            pytest.fail(
                f"Cannot test downward reactivity on constant '{meta.class_name}', "
                f"because constants do not have inner elements."
            )

    # 2) Composite must support decomposition
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}supports_decompose",
        verbose=verbose,
    ):
        if not meta.is_decomposeable:
            pytest.fail(
                f"Composite '{meta.class_name}' does not define a decomposition method, "
                f"downward reactivity cannot be tested."
            )

    # 3) Apply composite value change (validation + setter handled inside)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}apply_composite_value",
        verbose=verbose,
    ):
        assert_value_change(
            subtests,
            instance,
            value=new_value,
            verbose=verbose_value_change and verbose,
            intro=intro,
        )

    # 4) Expected inner values from decomposition
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compute_expected",
        verbose=verbose,
    ):
        try:
            expected_values = instance.decompose_value(new_value)
        except Exception as exc:
            pytest.fail(
                f"decompose_value raised an unexpected exception: {exc}"
            )

    # 5) Compare inner values with expected decomposed values
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_inners",
        verbose=verbose,
    ):
        for inner, expected_value in zip(meta.inners, expected_values):
            name_snake = inner.meta.name_snake
            actual_value = getattr(instance, name_snake)

            if actual_value != expected_value:
                pytest.fail(
                    f"Downward reactivity mismatch for inner '{name_snake}': "
                    f"expected {expected_value}, got {actual_value}"
                )
