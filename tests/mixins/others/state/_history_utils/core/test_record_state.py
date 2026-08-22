"""
Tests for `record_state(self)` (History core util).
"""
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.core import record_state


class TestRecordState:

    def test_returns_timestamp_snapshot_tuple(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        entry = record_state(instance)
        assert len(entry) == 2
        timestamp, snapshot = entry
        assert snapshot == instance._build_snapshot()

    def test_appends_to_history_list(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        original_count = len(instance._history)
        record_state(instance)
        assert len(instance._history) == original_count + 1

    def test_updates_history_count_and_index(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        record_state(instance)
        assert instance._history_count == len(instance._history)
        assert instance._history_index == instance._history_count - 1

    def test_respects_history_limit_fifo(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance._history_limit = 2
        record_state(instance)
        record_state(instance)
        assert len(instance._history) == 2