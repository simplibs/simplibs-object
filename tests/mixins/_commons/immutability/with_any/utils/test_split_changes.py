"""
Tests for `split_changes(self, changes)`.
"""
import pytest
from simplibs.object.mixins._common_logic.immutability.with_any.utils import (
    split_changes,
)


class TestSplitChanges:

    def test_all_constants(self, immutable_outer_instance):
        changes = (("first", 1), ("second", 2), ("third", 3))
        constants, composite = split_changes(immutable_outer_instance, changes)
        assert set(name for name, _ in constants) == {"first", "second", "third"}
        assert composite == ()

    def test_all_composite(self, immutable_outer_instance):
        changes = (("pair", 5),)
        constants, composite = split_changes(immutable_outer_instance, changes)
        assert constants == ()
        assert set(name for name, _ in composite) == {"pair"}

    def test_mixed_changes(self, immutable_outer_instance):
        changes = (("first", 1), ("pair", 5), ("third", 3))
        constants, composite = split_changes(immutable_outer_instance, changes)
        assert set(name for name, _ in constants) == {"first", "third"}
        assert set(name for name, _ in composite) == {"pair"}

    def test_returns_tuples(self, immutable_outer_instance):
        changes = (("first", 1),)
        result = split_changes(immutable_outer_instance, changes)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(item, tuple) for item in result)


class TestSplitChangesValidation:

    def test_unknown_name_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            split_changes(immutable_outer_instance, (("nonexistent", 1),))

    def test_invalid_inner_tuple_shape_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            split_changes(immutable_outer_instance, ((1, 2, 3),))

    def test_non_str_name_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            split_changes(immutable_outer_instance, ((123, "value"),))