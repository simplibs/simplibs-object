import pytest
from typing import Any, TYPE_CHECKING
from simplibs.exception.testing import maybe_subtest
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


def assert_calculate_value_method(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Deep validation gate for composite classes:
        - builds parameter map from inner defaults
        - calls calculate_value(...)
        - verifies that the computed value matches the class default
    """

    subintro = "test_calculate_value::"

    # 1) Prepare parameters for calculate_value
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_parameters",
        verbose=verbose,
    ):
        params = {
            inner.meta.name_snake: inner.meta.default
            for inner in test_class.meta.inners
        }
        assert params  # composite must have inners

    # 2) Compute composite value (runtime test of _logic)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}calculate_value",
        verbose=verbose,
    ):
        try:
            calculated = test_class.calculate_value(**params)
        except Exception as exc:
            pytest.fail(f"calculate_value raised an unexpected exception: {exc}")

    # 3) Compare computed value with class default
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_with_default",
        verbose=verbose,
    ):
        assert calculated == test_class.meta.default

