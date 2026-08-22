"""
Tests for `testing/asserts/methods/assert_calculate_value_method.py`.
"""
import pytest
from simplibs.object.testing.asserts.methods.assert_calculate_value_method import (
    assert_calculate_value_method,
)


class TestAssertCalculateValueMethodHappyPath:

    def test_passes_for_valid_composite_class(self, NonDecomposablePairObject, subtests):
        assert_calculate_value_method(subtests, NonDecomposablePairObject)

    def test_intro_and_verbose_do_not_affect_outcome(self, NonDecomposablePairObject, subtests):
        assert_calculate_value_method(
            subtests, NonDecomposablePairObject, verbose=False, intro="Suite::"
        )


class TestAssertCalculateValueMethodNoInners:

    def test_fails_when_class_has_no_inners(self, subtests):
        from types import SimpleNamespace

        fake_class = SimpleNamespace(
            __name__="FakeEmpty",
            meta=SimpleNamespace(inners=(), default=0),
        )

        with pytest.raises(pytest.fail.Exception, match="must define at least one inner component"):
            assert_calculate_value_method(
                subtests,
                fake_class,
                verbose=False,
            )