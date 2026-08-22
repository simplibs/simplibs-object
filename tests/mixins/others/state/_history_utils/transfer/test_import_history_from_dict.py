"""
Tests for `import_history_from_dict(self, history_dict)` (History transfer util).
"""
import pytest
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.transfer import (
    export_history_to_dict,
    import_history_from_dict,
)
from simplibs.object.mixins._common_logic.constants import OWNER_CLASS, HISTORY


class TestImportHistoryFromDict:

    def test_round_trip_export_import(self, IntLeaf):
        instance = IntLeaf(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        exported = export_history_to_dict(instance)

        other_instance = IntLeaf(mixins=(History,), mutable=True)
        import_history_from_dict(other_instance, exported)

        assert other_instance.history == exported[HISTORY]

    def test_jumps_to_last_entry_after_import(self, IntLeaf):
        instance = IntLeaf(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        exported = export_history_to_dict(instance)

        other_instance = IntLeaf(mixins=(History,), mutable=True)
        assert other_instance.value != 500

        import_history_from_dict(other_instance, exported)

        assert other_instance.value == 500


class TestImportHistoryFromDictValidation:

    def test_non_dict_input_raises(self, IntLeaf):
        instance = IntLeaf(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            import_history_from_dict(instance, "not_a_dict")

    def test_owner_class_mismatch_raises(self, IntLeaf):
        instance = IntLeaf(mixins=(History,), mutable=True)
        bad_dict = {OWNER_CLASS: "SomeOtherClass", HISTORY: ()}
        with pytest.raises(Exception):
            import_history_from_dict(instance, bad_dict)

    def test_rollback_on_failure_preserves_original_history(self, IntLeaf):
        """Verify original history is preserved via rollback if import fails."""
        instance = IntLeaf(mixins=(History,), mutable=True)
        instance.value = 500
        instance.record_state()
        original_history = instance.history

        broken_dict = {OWNER_CLASS: instance.meta.owner_class}

        with pytest.raises(Exception):
            import_history_from_dict(instance, broken_dict)

        assert instance.history == original_history