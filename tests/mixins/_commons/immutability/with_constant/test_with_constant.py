"""
Tests for `with_constant(self, name, new_value)`.
"""
import pytest
from simplibs.object.mixins._common_logic.immutability.with_constant import with_constant


class TestWithConstantHappyPath:

    def test_returns_new_instance(self, immutable_outer_instance):
        result = with_constant(immutable_outer_instance, "third", 30)
        assert result is not immutable_outer_instance

    def test_original_instance_unchanged(self, immutable_outer_instance):
        original_value = immutable_outer_instance.value
        with_constant(immutable_outer_instance, "third", 30)
        assert immutable_outer_instance.value == original_value

    def test_constant_value_updated(self, immutable_outer_instance):
        result = with_constant(immutable_outer_instance, "third", 30)
        assert result._nodes_dict["third"][0].value == 30

    def test_owner_value_recalculated(self, immutable_outer_instance):
        """
        Owner (Outer) logic is _logic(pair, third) = pair + third.
        third default is 3, pair default is (1+2)=3 => outer = 6.
        After updating third to 30, outer should be pair(3) + 30 = 33.
        """
        result = with_constant(immutable_outer_instance, "third", 30)
        assert result.value == 33

    def test_nested_constant_updates_immediate_owner_only(self, immutable_outer_instance):
        result = with_constant(immutable_outer_instance, "first", 10)
        pair_instance = result._nodes_dict["pair"][0]
        assert pair_instance.value == 10 + 2  # first(10) + second(2)


class TestWithConstantValidation:

    def test_unknown_name_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_constant(immutable_outer_instance, "nonexistent_name", 1)

    def test_invalid_value_type_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_constant(immutable_outer_instance, "third", "not_an_int")


class TestWithConstantMutableMode:

    def test_works_with_mutable_instance_too(self, mutable_outer_instance):
        result = with_constant(mutable_outer_instance, "third", 99)
        assert result is not mutable_outer_instance
        assert result.value == 99 + mutable_outer_instance._nodes_dict["pair"][0].value