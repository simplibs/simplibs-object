"""
Tests for `find_snapshot(self, ref)` (History core util).
"""
import pytest
from datetime import datetime, timedelta
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.core import find_snapshot


class TestFindSnapshotByIndex:

    def test_valid_index_returns_snapshot(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 100
        instance.record_state()

        result = find_snapshot(instance, 0)
        assert result == instance._history[0][1]

    def test_negative_index_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            find_snapshot(instance, -1)

    def test_out_of_range_index_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            find_snapshot(instance, 999)


class TestFindSnapshotByTimestamp:

    def test_matching_timestamp_returns_snapshot(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        timestamp, snapshot = instance._history[0]

        result = find_snapshot(instance, timestamp)
        assert result == snapshot

    def test_unmatched_timestamp_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        fake_timestamp = datetime.now() + timedelta(days=999)
        with pytest.raises(Exception):
            find_snapshot(instance, fake_timestamp)


class TestFindSnapshotInvalidRef:

    def test_invalid_ref_type_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            find_snapshot(instance, "not_an_index_or_timestamp")