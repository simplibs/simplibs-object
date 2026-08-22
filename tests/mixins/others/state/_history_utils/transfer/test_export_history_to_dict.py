"""
Tests for `export_history_to_dict(self)` (History transfer util).
"""
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.transfer import (
    export_history_to_dict,
)
from simplibs.object.mixins._common_logic.constants import OWNER_CLASS, HISTORY


class TestExportHistoryToDict:

    def test_contains_owner_class(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        result = export_history_to_dict(instance)
        assert result[OWNER_CLASS] == instance.meta.owner_class

    def test_contains_history_tuple(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        result = export_history_to_dict(instance)
        assert result[HISTORY] == instance.history

    def test_history_matches_current_state(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()

        result = export_history_to_dict(instance)

        assert len(result[HISTORY]) == 2