"""
Tests for `go_to_history_on_timestamp(self, timestamp)` (History navigation util).
"""
import pytest
from datetime import datetime, timedelta
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.navigations import (
    go_to_history_on_timestamp,
)


class TestGoToHistoryOnTimestamp:

    def test_matching_timestamp_restores_snapshot(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        first_timestamp = instance._history[0][0]
        original_value = instance.value

        instance.value = 500
        instance.record_state()

        go_to_history_on_timestamp(instance, first_timestamp)

        assert instance.value == original_value
        assert instance._history_index == 0

    def test_unmatched_timestamp_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        fake_timestamp = datetime.now() + timedelta(days=999)
        with pytest.raises(Exception):
            go_to_history_on_timestamp(instance, fake_timestamp)

    def test_non_datetime_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            go_to_history_on_timestamp(instance, "not_a_datetime")