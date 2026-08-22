"""
Tests for `with_constants(self, changes)`.
"""
import pytest
from simplibs.object.mixins._common_logic.immutability.with_constants import with_constants


class TestWithConstantsNoChanges:

    def test_no_changes_returns_equivalent_new_instance(self, immutable_outer_instance):
        result = with_constants(immutable_outer_instance)
        assert result is not immutable_outer_instance
        assert result.value == immutable_outer_instance.value

    def test_none_changes_returns_equivalent_new_instance(self, immutable_outer_instance):
        result = with_constants(immutable_outer_instance, None)
        assert result.value == immutable_outer_instance.value


class TestWithConstantsSingleChange:

    def test_single_change_as_tuple(self, immutable_outer_instance):
        result = with_constants(immutable_outer_instance, ("third", 50))
        assert result._nodes_dict["third"][0].value == 50

    def test_owner_recalculated_for_single_change(self, immutable_outer_instance):
        result = with_constants(immutable_outer_instance, ("third", 50))
        # outer = pair(3) + third(50) = 53
        assert result.value == 53


class TestWithConstantsMultipleChanges:

    def test_multiple_changes_all_applied(self, immutable_outer_instance):
        result = with_constants(
            immutable_outer_instance,
            (("first", 10), ("second", 20), ("third", 30)),
        )
        assert result._nodes_dict["first"][0].value == 10
        assert result._nodes_dict["second"][0].value == 20
        assert result._nodes_dict["third"][0].value == 30

    def test_owners_recalculated_from_deepest_nodes(self, immutable_outer_instance):
        result = with_constants(
            immutable_outer_instance,
            (("first", 10), ("second", 20)),
        )
        assert result._nodes_dict["pair"][0].value == 30  # 10 + 20
        assert result.value == 30 + 3  # pair(30) + third(default 3)

    def test_original_instance_unchanged(self, immutable_outer_instance):
        original_value = immutable_outer_instance.value
        with_constants(immutable_outer_instance, (("third", 999),))
        assert immutable_outer_instance.value == original_value


class TestWithConstantsValidation:

    def test_changes_not_tuple_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_constants(immutable_outer_instance, ["third", 5])

    def test_unknown_constant_name_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_constants(immutable_outer_instance, ("nonexistent", 5))

    def test_composite_name_in_changes_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_constants(immutable_outer_instance, ("pair", 5))

    def test_invalid_inner_tuple_shape_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_constants(immutable_outer_instance, (("third", 1, 2),))