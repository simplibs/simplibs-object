"""
Tests for `process_single_change(self, change)`.
"""
import pytest
from simplibs.object.mixins._common_logic.immutability.with_any.utils import (
    process_single_change,
)


class TestProcessSingleChangeHappyPath:

    def test_constant_change_delegates_correctly(self, immutable_outer_instance):
        result = process_single_change(immutable_outer_instance, ("third", 42))
        assert result._nodes_dict["third"][0].value == 42

    def test_composite_change_delegates_correctly(self, immutable_outer_instance):
        result = process_single_change(immutable_outer_instance, ("pair", 15))
        assert result._nodes_dict["pair"][0].value == 15

    def test_returns_new_instance(self, immutable_outer_instance):
        result = process_single_change(immutable_outer_instance, ("third", 1))
        assert result is not immutable_outer_instance


class TestProcessSingleChangeValidation:

    def test_unknown_name_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            process_single_change(immutable_outer_instance, ("nonexistent", 1))

    def test_malformed_change_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            process_single_change(immutable_outer_instance, ("only_one_item",))