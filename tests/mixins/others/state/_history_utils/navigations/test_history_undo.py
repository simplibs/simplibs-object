"""
Tests for `history_undo(self)` (History navigation util).
"""
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.navigations import history_undo


class TestHistoryUndo:

    def test_no_previous_entry_returns_false(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert history_undo(instance) is False

    def test_moves_to_previous_entry(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        original_value = instance.value
        instance.value = 500
        instance.record_state()

        result = history_undo(instance)

        assert result is True
        assert instance.value == original_value

    def test_decrements_history_index(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        original_index = instance._history_index

        history_undo(instance)

        assert instance._history_index == original_index - 1