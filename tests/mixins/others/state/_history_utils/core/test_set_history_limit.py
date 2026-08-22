"""
Tests for `set_history_limit(self, value)` (History core util).
"""
import pytest
from simplibs.object.mixins.others.state import History
from simplibs.object.mixins.others.state._history_utils.core import set_history_limit


class TestSetHistoryLimit:

    def test_sets_limit_value(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        set_history_limit(instance, 5)
        assert instance._history_limit == 5

    def test_trims_existing_history_to_new_limit(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        for i in range(5):
            instance.value = i
            instance.record_state()
        assert len(instance._history) == 6

        set_history_limit(instance, 2)

        assert len(instance._history) == 2
        assert instance._history_count == 2
        assert instance._history_index == 1

    def test_no_trim_when_history_below_limit(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        set_history_limit(instance, 100)
        assert len(instance._history) == 1


class TestSetHistoryLimitValidation:

    def test_zero_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            set_history_limit(instance, 0)

    def test_negative_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            set_history_limit(instance, -5)

    def test_non_int_raises(self, Outer):
        instance = Outer(mixins=(History,), mutable=True)
        with pytest.raises(Exception):
            set_history_limit(instance, "five")