"""
Tests for `go_to_last_history(self)` (History navigation util).
"""
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.navigations import (
    go_to_last_history,
    history_undo,
)


class TestGoToLastHistory:

    def test_noop_when_already_at_last(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        original_index = instance._history_index
        go_to_last_history(instance)
        assert instance._history_index == original_index

    def test_jumps_to_last_after_undo(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        history_undo(instance)
        assert instance.value != 500

        go_to_last_history(instance)

        assert instance._history_index == instance._history_count - 1
        assert instance.value == 500