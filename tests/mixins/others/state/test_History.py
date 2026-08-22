"""
Tests for `History` mixin.
"""
import pytest
from datetime import datetime
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.core_mixins import Serialization
from simplibs.object.testing import assert_simple_mixin


class TestHistoryStructure:

    def test_mutable_only_flag(self):
        assert History._mutable_only is True

    def test_inherits_from_serialization(self):
        assert issubclass(History, Serialization)

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            History,
            test_class=Outer,
            slots_names=(
                "_history",
                "_history_index",
                "_history_limit",
                "_history_count",
            ),
            attribute_names=("history", "history_index", "history_limit"),
            method_names=(
                "record_state",
                "undo",
                "redo",
                "go_to_last",
                "go_to_index",
                "go_to_timestamp",
                "export_history_to_dict",
                "import_history_from_dict",
                "remove_history_limit",
                "diff",
            ),
        )


class TestHistoryInitialization:

    def test_starts_with_one_entry(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert len(instance.history) == 1

    def test_history_limit_starts_none(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert instance.history_limit is None

    def test_history_index_starts_at_zero(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert instance.history_index == 0


class TestHistoryRecordAndUndoRedo:

    def test_record_state_adds_entry(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        assert len(instance.history) == 2

    def test_undo_restores_previous_value(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        original_value = instance.value
        instance.value = 500
        instance.record_state()

        assert instance.undo() is True
        assert instance.value == original_value

    def test_redo_after_undo_restores_value(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        instance.undo()

        assert instance.redo() is True
        assert instance.value == 500

    def test_undo_at_start_returns_false(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert instance.undo() is False

    def test_redo_at_end_returns_false(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        assert instance.redo() is False


class TestHistoryGoTo:

    def test_go_to_index(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        original_value = instance.value
        instance.value = 500
        instance.record_state()

        instance.go_to_index(0)

        assert instance.value == original_value

    def test_go_to_last(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        instance.go_to_index(0)

        instance.go_to_last()

        assert instance.value == 500

    def test_go_to_timestamp(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        first_timestamp = instance.history[0][0]
        instance.value = 500
        instance.record_state()

        instance.go_to_timestamp(first_timestamp)

        assert instance.history_index == 0


class TestHistoryLimit:

    def test_history_limit_setter(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.history_limit = 3
        assert instance.history_limit == 3

    def test_remove_history_limit(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.history_limit = 3
        instance.remove_history_limit()
        assert instance.history_limit is None


class TestHistoryExportImport:

    def test_export_returns_dict(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        result = instance.export_history_to_dict()
        assert isinstance(result, dict)

    def test_import_round_trip(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        exported = instance.export_history_to_dict()

        other = Outer(mixins=(History,), mutable=True)
        other.import_history_from_dict(exported)

        assert other.value == 500


class TestHistoryDiff:

    def test_diff_between_indices(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()

        result = instance.diff(0, 1)

        assert len(result) > 0

    def test_diff_identical_indices_empty(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        result = instance.diff(0, 0)
        assert result == ()


class TestHistoryCompatibility:

    def test_rejects_immutable_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(History,), mutable=False)