"""
Tests for the guards added to the object testing helpers: an immutability check with a value that proves
nothing, and a class-inheritance check given something that is not a class.
"""
import pytest
from _pytest.outcomes import Failed

from simplibs.object.testing.asserts.base.assert_class_inheritance import assert_class_inheritance
from simplibs.object.testing.asserts.mutability.assert_immutable_behavior import assert_immutable_behavior


class TestImmutabilityNeedsAnAcceptableValue:

    def test_an_invalid_value_is_rejected_by_the_check_itself(self, PositiveIntConst, subtests):
        """Verify that a value the class would reject anyway cannot 'prove' immutability."""
        with pytest.raises(Failed, match="invalid"):
            assert_immutable_behavior(subtests, PositiveIntConst, new_value=-5, verbose=False)

    def test_a_value_equal_to_the_current_one_is_rejected_by_the_check_itself(self, IntConst, subtests):
        """Verify that an assignment which would be invisible cannot 'prove' immutability."""
        with pytest.raises(Failed, match="equals the current value"):
            assert_immutable_behavior(subtests, IntConst, new_value=0, verbose=False)  # the default is 0

    def test_a_valid_different_value_still_passes(self, IntConst, subtests):
        assert_immutable_behavior(subtests, IntConst, new_value=99, verbose=False)


class TestClassInheritanceGivenANonClass:

    def test_something_that_is_not_a_class_is_a_failed_check(self, subtests):
        """Verify an AssertionError with a message, not a TypeError from issubclass."""
        with pytest.raises(AssertionError, match="derived from SimpleConstant"):
            assert_class_inheritance(subtests, "not-a-class", verbose=False)
