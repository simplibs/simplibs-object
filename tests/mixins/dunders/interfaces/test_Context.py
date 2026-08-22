"""
Tests for `ContextManager` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.interfaces import ContextManager
from simplibs.object.testing import assert_simple_mixin


class TestContextManagerStructure:

    def test_slots_empty(self):
        assert ContextManager.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            ContextManager,
            test_class=IntLeaf,
            method_names=("__enter__", "__exit__"),
        )


class TestContextManagerBehavior:

    def test_enter_returns_self(self, IntLeaf):
        instance = IntLeaf(mixins=(ContextManager,), as_atom=True)
        with instance as ctx:
            assert ctx is instance

    def test_exit_does_not_suppress_exceptions(self, IntLeaf):
        instance = IntLeaf(mixins=(ContextManager,), as_atom=True)
        with pytest.raises(ValueError):
            with instance:
                raise ValueError("boom")

    def test_no_state_change_from_context_usage(self, IntLeaf):
        instance = IntLeaf(mixins=(ContextManager,), as_atom=True)
        original_value = instance.value
        with instance:
            pass
        assert instance.value == original_value