"""
Tests for `Copyable` mixin.
"""
import copy
import pytest
from simplibs.object.mixins.core_mixins import NodesDicts, Snapshot
from simplibs.object.mixins.dunders.lifecycles import Copyable
from simplibs.object.testing import assert_simple_mixin


class TestCopyableStructure:

    def test_inherits_from_nodes_dicts_and_snapshot(self):
        assert issubclass(Copyable, NodesDicts)
        assert issubclass(Copyable, Snapshot)

    def test_slots_empty(self):
        assert Copyable.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Copyable,
            test_class=Outer,
            method_names=("__copy__", "__deepcopy__"),
        )


class TestCopyableShallowCopy:

    def test_copy_returns_new_instance(self, Outer):
        instance = Outer(mixins=(Copyable,), mutable=False)
        result = copy.copy(instance)
        assert result is not instance

    def test_copy_matches_original_state(self, Outer):
        instance = Outer(mixins=(Copyable,), mutable=False)
        result = copy.copy(instance)
        assert result._build_snapshot() == instance._build_snapshot()

    def test_copy_works_for_mutable_instance(self, Outer):
        instance = Outer(mixins=(Copyable,), mutable=True)
        result = copy.copy(instance)
        assert result is not instance
        assert result._build_snapshot() == instance._build_snapshot()


class TestCopyableDeepCopy:

    def test_deepcopy_returns_new_instance(self, Outer):
        instance = Outer(mixins=(Copyable,), mutable=False)
        result = copy.deepcopy(instance)
        assert result is not instance
        assert result._build_snapshot() == instance._build_snapshot()

    def test_deepcopy_via_direct_dunder_call(self, Outer):
        instance = Outer(mixins=(Copyable,), mutable=False)
        result = instance.__deepcopy__({})
        assert result._build_snapshot() == instance._build_snapshot()