"""
Tests for `history_redo(self)` (History navigation util).
"""
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.navigations import (
    history_redo,
    history_undo,
)


class TestHistoryRedo:

    def test_no_next_entry_returns_false(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert history_redo(instance) is False

    def test_moves_forward_after_undo(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        history_undo(instance)

        result = history_redo(instance)

        assert result is True
        assert instance.value == 500

    def test_increments_history_index(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        history_undo(instance)
        index_after_undo = instance._history_index

        history_redo(instance)

        assert instance._history_index == index_after_undo + 1