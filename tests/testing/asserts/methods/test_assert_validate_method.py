"""
Tests for `testing/asserts/methods/assert_validate_method.py`.
"""
from simplibs.object.testing.asserts.methods.assert_validate_method import (
    assert_validate_method,
)


class TestAssertValidateMethodHappyPath:

    def test_passes_for_plain_constant_class(self, IntConst, subtests):
        assert_validate_method(subtests, IntConst)

    def test_passes_for_composite_class(self, NonDecomposablePairObject, subtests):
        assert_validate_method(subtests, NonDecomposablePairObject)

    def test_passes_for_class_with_custom_validate(self, PositiveIntConst, subtests):
        assert_validate_method(subtests, PositiveIntConst)


class TestAssertValidateMethodIntroVerbose:

    def test_intro_and_verbose_do_not_affect_outcome(self, IntConst, subtests):
        assert_validate_method(subtests, IntConst, verbose=False, intro="Suite::")