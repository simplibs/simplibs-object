"""
Tests for `testing/asserts/reactivity/assert_reactivity_downward.py`.
"""
import pytest
from simplibs.object.testing.asserts.reactivity.assert_reactivity_downward import (
    assert_reactivity_downward,
)


class TestAssertReactivityDownwardHappyPath:

    def test_passes_for_decomposeable_composite(self, PairObject, subtests):
        instance = PairObject(mixins=())
        assert_reactivity_downward(subtests, instance, new_value=5)

    def test_inner_properties_reflect_decomposed_state(self, PairObject, subtests):
        instance = PairObject(mixins=())
        assert_reactivity_downward(subtests, instance, new_value=8)

        expected = instance.decompose_value(8)
        assert (instance.first, instance.second) == expected


class TestAssertReactivityDownwardNotComposite:

    def test_fails_on_atomic_constant(self, IntConst, subtests):
        instance = IntConst()
        with pytest.raises(BaseException):
            assert_reactivity_downward(subtests, instance, new_value=5, verbose=False)


class TestAssertReactivityDownwardNotDecomposeable:

    def test_fails_on_non_decomposeable_composite(self, NonDecomposablePairObject, subtests):
        instance = NonDecomposablePairObject(mixins=())
        with pytest.raises(BaseException):
            assert_reactivity_downward(subtests, instance, new_value=5, verbose=False)