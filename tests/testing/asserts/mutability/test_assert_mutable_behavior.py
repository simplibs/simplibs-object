"""
Tests for `testing/asserts/mutability/assert_mutable_behavior.py`.
"""
from simplibs.object.testing.asserts.mutability.assert_mutable_behavior import (
    assert_mutable_behavior,
)


class TestAssertMutableBehaviorHappyPath:

    def test_passes_for_correctly_mutable_constant(self, IntConst, subtests):
        assert_mutable_behavior(subtests, IntConst, new_value=99)

    def test_intro_and_verbose_do_not_affect_outcome(self, IntConst, subtests):
        assert_mutable_behavior(
            subtests, IntConst, new_value=42, verbose=False, intro="Suite::"
        )

    def test_verbose_value_change_flag_is_forwarded(self, IntConst, subtests):
        assert_mutable_behavior(
            subtests, IntConst, new_value=7, verbose_value_change=False
        )