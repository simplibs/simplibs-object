"""
Tests for `go_to_history_on_index(self, index)` (History navigation util).
"""
import pytest
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.navigations import (
    go_to_history_on_index,
)


class TestGoToHistoryOnIndex:

    def test_valid_index_restores_snapshot(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        original_value = instance.value
        instance.value = 500
        instance.record_state()

        go_to_history_on_index(instance, 0)

        assert instance.value == original_value
        assert instance._history_index == 0

    def test_negative_index_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            go_to_history_on_index(instance, -1)

    def test_out_of_range_index_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            go_to_history_on_index(instance, 100)