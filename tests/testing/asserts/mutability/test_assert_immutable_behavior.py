"""
Tests for `testing/asserts/mutability/assert_immutable_behavior.py`.
"""
from simplibs.object.testing.asserts.mutability.assert_immutable_behavior import (
    assert_immutable_behavior,
)


class TestAssertImmutableBehaviorHappyPath:

    def test_passes_for_correctly_immutable_constant(self, IntConst, subtests):
        assert_immutable_behavior(subtests, IntConst, new_value=99)

    def test_intro_and_verbose_do_not_affect_outcome(self, IntConst, subtests):
        assert_immutable_behavior(
            subtests, IntConst, new_value=42, verbose=False, intro="Suite::"
        )