"""
Tests for `ClassGetItem` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.generics import ClassGetItem
from simplibs.object.testing import assert_simple_mixin


class TestClassGetItemStructure:

    def test_slots_empty(self):
        assert ClassGetItem.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(subtests, ClassGetItem, test_class=IntLeaf)


class TestClassGetItemBehavior:

    def test_subscript_returns_class_itself_when_no_parent_impl(self, IntLeaf):
        instance = IntLeaf(mixins=(ClassGetItem,), as_atom=True)
        result = type(instance)[int]
        assert result is type(instance)

    def test_subscript_with_various_items(self, IntLeaf):
        instance = IntLeaf(mixins=(ClassGetItem,), as_atom=True)
        cls = type(instance)
        assert cls[str] is cls
        assert cls[(int, str)] is cls