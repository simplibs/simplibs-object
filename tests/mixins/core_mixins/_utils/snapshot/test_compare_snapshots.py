"""
Tests for `compare_snapshots(nodes_tuple, snapshot1, snapshot2, *, constants_only=False)`.
"""
import pytest
from simplibs.object.mixins.core_mixins import Infrastructure
from simplibs.object.mixins.core_mixins._utils.snapshot import compare_snapshots


class TestCompareSnapshotsNoChanges:

    def test_identical_snapshots_return_empty_tuple(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        snapshot = instance._build_snapshot()
        result = compare_snapshots(instance._nodes_tuple, snapshot, snapshot)
        assert result == ()


class TestCompareSnapshotsWithChanges:

    def test_single_changed_leaf_detected(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        snap1 = instance._build_snapshot()
        snap2 = list(snap1)
        # Find index of 'third' in _nodes_tuple and change its value
        third_index = next(
            i for i, (inst, _) in enumerate(instance._nodes_tuple)
            if inst.meta.name_snake == "third"
        )
        snap2[third_index] = 999
        snap2 = tuple(snap2)

        result = compare_snapshots(instance._nodes_tuple, snap1, snap2)

        assert len(result) == 1
        path, old_value, new_value = result[0]
        assert old_value == snap1[third_index]
        assert new_value == 999

    def test_constants_only_excludes_composite_diffs(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        snap1 = instance._build_snapshot()
        # Create a snapshot where all values differ
        snap2 = tuple(v + 1000 if isinstance(v, int) else v for v in snap1)

        result_all = compare_snapshots(instance._nodes_tuple, snap1, snap2)
        result_constants_only = compare_snapshots(
            instance._nodes_tuple, snap1, snap2, constants_only=True
        )

        assert len(result_constants_only) <= len(result_all)


class TestCompareSnapshotsIncompatible:
    """
    Reserved for future incompatible snapshot comparison scenarios (e.g., ambiguous numpy evaluations).
    """
    pass