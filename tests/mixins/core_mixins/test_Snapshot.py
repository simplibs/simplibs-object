"""
Tests for `Snapshot` mixin.
"""
from simplibs.object.mixins.core_mixins import Snapshot
from simplibs.object.testing import assert_simple_mixin


class TestSnapshotStructure:

    def test_method_names_present(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Snapshot,
            test_class=Outer,
            method_names=("_build_snapshot", "_restore_snapshot", "_compare_snapshots"),
        )


class TestSnapshotBuildRestore:

    def test_build_snapshot_returns_tuple_of_values(self, Outer):
        instance = Outer(mixins=(Snapshot,))
        snapshot = instance._build_snapshot()
        assert isinstance(snapshot, tuple)
        assert len(snapshot) == len(instance._nodes_tuple)

    def test_build_snapshot_matches_current_values(self, Outer):
        instance = Outer(mixins=(Snapshot,))
        snapshot = instance._build_snapshot()
        expected = tuple(inst.value for inst, _ in instance._nodes_tuple)
        assert snapshot == expected

    def test_restore_snapshot_writes_values_back(self, Outer):
        instance = Outer(mixins=(Snapshot,), mutable=True)
        original_snapshot = instance._build_snapshot()

        for inst, _ in instance._nodes_tuple:
            inst._value = inst._value

        modified_snapshot = tuple(
            v + 500 if isinstance(v, int) else v for v in original_snapshot
        )
        instance._restore_snapshot(modified_snapshot)

        assert instance._build_snapshot() == modified_snapshot

    def test_restore_then_rebuild_round_trip(self, Outer):
        instance = Outer(mixins=(Snapshot,), mutable=True)
        snapshot = instance._build_snapshot()
        instance._restore_snapshot(snapshot)
        assert instance._build_snapshot() == snapshot


class TestSnapshotCompare:

    def test_compare_identical_snapshots_empty(self, Outer):
        instance = Outer(mixins=(Snapshot,))
        snapshot = instance._build_snapshot()
        assert instance._compare_snapshots(snapshot, snapshot) == ()

    def test_compare_delegates_to_util_correctly(self, Outer):
        instance = Outer(mixins=(Snapshot,))
        snap1 = instance._build_snapshot()
        snap2 = tuple(v + 1 if isinstance(v, int) else v for v in snap1)
        result = instance._compare_snapshots(snap1, snap2)
        assert len(result) > 0
        for _, old_value, new_value in result:
            assert old_value != new_value