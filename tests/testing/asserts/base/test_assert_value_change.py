"""
Tests for `testing/asserts/base/assert_value_change.py`.
"""
import pytest
from simplibs.object.testing.asserts.base.assert_value_change import assert_value_change
from simplibs.object.testing.containers.InnerValue import InnerValue


class TestAssertValueChangeDirectValue:

    def test_changes_root_value_successfully(self, IntConst, subtests):
        instance = IntConst()
        result = assert_value_change(subtests, instance, value=42)

        assert result == 42
        assert instance.value == 42

    def test_returns_the_applied_value(self, IntConst, subtests):
        instance = IntConst()
        result = assert_value_change(subtests, instance, value=7)
        assert result == 7


class TestAssertValueChangeInnerValue:

    def test_changes_nested_inner_value(self, NonDecomposablePairObject, subtests):
        instance = NonDecomposablePairObject(mixins=())
        iv = InnerValue(path="first", value=999)

        result = assert_value_change(subtests, instance, value=iv)
        assert result == 999
        assert instance.first == 999


class TestAssertValueChangeSameValueFails:

    def test_same_value_as_current_state_fails(self, IntConst, subtests):
        instance = IntConst()
        current = instance.value

        with pytest.raises(pytest.fail.Exception, match="New value must differ from current state value"):
            assert_value_change(
                subtests,
                instance,
                value=current,
                verbose=False,
            )