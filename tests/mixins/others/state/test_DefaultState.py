"""
Tests for `DefaultState` mixin.
"""
import pytest
from simplibs.object.mixins.others.state import DefaultState
from simplibs.object.mixins.core_mixins import Snapshot
from simplibs.object.testing import assert_simple_mixin


class TestDefaultStateStructure:

    def test_mutable_only_flag(self):
        assert DefaultState._mutable_only is True

    def test_inherits_from_snapshot(self):
        assert issubclass(DefaultState, Snapshot)

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            DefaultState,
            test_class=Outer,
            slots_names=("_default_state_snapshot",),
            method_names=(
                "clone_instance",
                "reset_to_default_values",
                "create_new_default_instance",
            ),
        )


class TestDefaultStateSnapshotCapture:

    def test_default_state_captured_at_init(self, Outer):
        instance = Outer(mixins=(DefaultState,), mutable=True)
        assert instance._default_state_snapshot == instance._build_snapshot()


class TestDefaultStateResetToDefaultValues:

    def test_reset_restores_initial_state(self, Outer):
        instance = Outer(mixins=(DefaultState,), mutable=True)
        original_snapshot = instance._build_snapshot()
        instance.value = 999

        instance.reset_to_default_values()

        assert instance._build_snapshot() == original_snapshot


class TestDefaultStateCreateNewDefaultInstance:

    def test_returns_new_instance_matching_original_default(self, Outer):
        instance = Outer(mixins=(DefaultState,), mutable=True)
        default_snapshot = instance._default_state_snapshot
        instance.value = 999

        new_instance = instance.create_new_default_instance()

        assert new_instance is not instance
        assert new_instance._build_snapshot() == default_snapshot


class TestDefaultStateCloneInstance:

    def test_clone_matches_current_state_not_default(self, Outer):
        instance = Outer(mixins=(DefaultState,), mutable=True)
        instance.value = 777

        clone = instance.clone_instance()

        assert clone is not instance
        assert clone._build_snapshot() == instance._build_snapshot()

    def test_clone_differs_from_default_after_changes(self, Outer):
        instance = Outer(mixins=(DefaultState,), mutable=True)
        default_snapshot = instance._default_state_snapshot
        instance.value = 777

        clone = instance.clone_instance()

        assert clone._build_snapshot() != default_snapshot


class TestDefaultStateCompatibility:

    def test_rejects_immutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(DefaultState,), mutable=False)