"""
Tests for `DirtyTracking` mixin.
"""
import pytest
from simplibs.object.mixins.others.state import DirtyTracking
from simplibs.object.mixins.core_mixins import Snapshot
from simplibs.object.testing import assert_simple_mixin


class TestDirtyTrackingStructure:

    def test_mutable_only_flag(self):
        assert DirtyTracking._mutable_only is True

    def test_inherits_from_snapshot(self):
        assert issubclass(DirtyTracking, Snapshot)

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            DirtyTracking,
            test_class=Outer,
            slots_names=("_clean_snapshot",),
            attribute_names=("is_dirty", "dirty_paths", "clean_snapshot"),
            method_names=("get_dirty_paths", "reset_to_clean", "mark_clean"),
        )


class TestDirtyTrackingIsDirty:

    def test_starts_clean(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        assert instance.is_dirty is False

    def test_becomes_dirty_after_change(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        instance.value = 999
        assert instance.is_dirty is True


class TestDirtyTrackingPaths:

    def test_dirty_paths_empty_when_clean(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        assert instance.dirty_paths == ()

    def test_dirty_paths_non_empty_after_change(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        instance.value = 999
        assert len(instance.dirty_paths) > 0

    def test_get_dirty_paths_constants_only_false_includes_composites(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        instance.value = 999
        all_paths = instance.get_dirty_paths(constants_only=False)
        constants_paths = instance.get_dirty_paths(constants_only=True)
        assert len(all_paths) >= len(constants_paths)


class TestDirtyTrackingResetAndMark:

    def test_reset_to_clean_restores_snapshot(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        clean_snapshot = instance.clean_snapshot
        instance.value = 999

        instance.reset_to_clean()

        assert instance._build_snapshot() == clean_snapshot
        assert instance.is_dirty is False

    def test_mark_clean_updates_baseline(self, Outer):
        instance = Outer(mixins=(DirtyTracking,), mutable=True)
        instance.value = 999
        assert instance.is_dirty is True

        instance.mark_clean()

        assert instance.is_dirty is False
        assert instance.clean_snapshot == instance._build_snapshot()


class TestDirtyTrackingCompatibility:

    def test_rejects_immutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(DirtyTracking,), mutable=False)