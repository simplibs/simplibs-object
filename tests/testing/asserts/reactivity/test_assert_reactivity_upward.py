"""
Tests for `testing/asserts/reactivity/assert_reactivity_upward.py`.
"""
import pytest
from simplibs.object.testing.asserts.reactivity.assert_reactivity_upward import (
    assert_reactivity_upward,
)
from simplibs.object.testing.containers.InnerValue import InnerValue


class TestAssertReactivityUpwardHappyPath:

    def test_passes_when_inner_change_propagates_to_root(
        self, NonDecomposablePairObject, subtests
    ):
        instance = NonDecomposablePairObject(mixins=())
        iv = InnerValue(path="first", value=instance.first + 1)

        assert_reactivity_upward(subtests, instance, new_value=iv)

    def test_root_value_reflects_new_sum(self, NonDecomposablePairObject, subtests):
        instance = NonDecomposablePairObject(mixins=())
        original_second = instance.second
        iv = InnerValue(path="first", value=50)

        assert_reactivity_upward(subtests, instance, new_value=iv)
        assert instance.value == 50 + original_second


class TestAssertReactivityUpwardRequiresInnerValue:

    def test_raw_value_instead_of_inner_value_fails(
        self, NonDecomposablePairObject, subtests
    ):
        instance = NonDecomposablePairObject(mixins=())
        with pytest.raises(BaseException):
            assert_reactivity_upward(subtests, instance, new_value=5, verbose=False)


class TestAssertReactivityUpwardNoChange:

    def test_fails_when_inner_value_does_not_actually_change_root(
        self, NonDecomposablePairObject, subtests
    ):
        instance = NonDecomposablePairObject(mixins=())
        iv = InnerValue(path="first", value=instance.first)

        with pytest.raises(BaseException):
            assert_reactivity_upward(subtests, instance, new_value=iv, verbose=False)