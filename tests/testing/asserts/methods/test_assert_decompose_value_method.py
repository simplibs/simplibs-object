"""
Tests for `testing/asserts/methods/assert_decompose_value_method.py`.
"""
import pytest
from simplibs.object.testing.asserts.methods.assert_decompose_value_method import (
    assert_decompose_value_method,
)


class TestAssertDecomposeValueMethodHappyPath:

    def test_passes_for_valid_decomposeable_class(self, PairObject, subtests):
        assert_decompose_value_method(subtests, PairObject)

    def test_intro_and_verbose_do_not_affect_outcome(self, PairObject, subtests):
        assert_decompose_value_method(
            subtests, PairObject, verbose=False, intro="Suite::"
        )


class TestAssertDecomposeValueMethodNoInners:

    def test_fails_when_class_has_no_inners(self, subtests):
        from types import SimpleNamespace

        fake_class = SimpleNamespace(
            __name__="FakeEmpty",
            meta=SimpleNamespace(inners=(), default=0),
            decompose_value=lambda value: (),
        )

        with pytest.raises(pytest.fail.Exception, match="must define at least one inner component"):
            assert_decompose_value_method(
                subtests,
                fake_class,
                verbose=False,
            )


class TestAssertDecomposeValueMethodMismatch:

    def test_fails_when_decompose_result_does_not_match_expected_defaults(self, subtests):
        from types import SimpleNamespace

        fake_inner = SimpleNamespace(meta=SimpleNamespace(name_snake="first", default=1))
        fake_class = SimpleNamespace(
            __name__="FakeMismatch",
            meta=SimpleNamespace(inners=(fake_inner,), default=99),
            decompose_value=lambda value: (999,),
        )

        with pytest.raises(pytest.fail.Exception, match="does not match expected inner defaults"):
            assert_decompose_value_method(
                subtests,
                fake_class,
                verbose=False,
            )