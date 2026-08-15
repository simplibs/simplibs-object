from typing import Any, TYPE_CHECKING
import pytest
from simplibs.exception.testing import maybe_subtest
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols import SimpleClassLike


def assert_decompose_value_method(
    subtests: Any,
    test_class: "SimpleClassLike",
    *,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """
    Deep validation gate for composite classes that support decomposition:
        - calls decompose_value(default)
        - verifies that the decomposed tuple matches inner defaults
    """

    subintro = "test_decompose_value::"

    # 1. Prepare expected decomposed values
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}prepare_expected",
        verbose=verbose,
    ):
        expected = tuple(inner.meta.default for inner in test_class.meta.inners)
        assert expected  # composite must have inners

    # 2. Compute decomposed value (runtime test of _decompose)
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}decompose_value",
        verbose=verbose,
    ):
        try:
            decomposed = test_class.decompose_value(test_class.meta.default)
        except Exception as exc:
            pytest.fail(f"decompose_value raised an unexpected exception: {exc}")

    # 3. Compare decomposed value with expected inner defaults
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}compare_with_expected",
        verbose=verbose,
    ):
        assert decomposed == expected
