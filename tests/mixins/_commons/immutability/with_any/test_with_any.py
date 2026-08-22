"""
Tests for `with_any(self, changes)`.
"""
import pytest
from simplibs.object.mixins._common_logic.immutability.with_any import with_any


class TestWithAnyNoChanges:

    def test_none_returns_new_instance_for_immutable(self, immutable_outer_instance):
        result = with_any(immutable_outer_instance, None)
        assert result is not immutable_outer_instance
        assert result.value == immutable_outer_instance.value

    def test_empty_default_returns_new_instance(self, immutable_outer_instance):
        result = with_any(immutable_outer_instance)
        assert result.value == immutable_outer_instance.value

    def test_mutable_mode_returns_value_not_instance(self, mutable_outer_instance):
        result = with_any(mutable_outer_instance, None)
        assert result == mutable_outer_instance.value
        assert not hasattr(result, "_nodes_tuple")


class TestWithAnySingleChange:

    def test_single_constant_change(self, immutable_outer_instance):
        result = with_any(immutable_outer_instance, ("third", 42))
        assert result._nodes_dict["third"][0].value == 42

    def test_single_composite_change(self, immutable_outer_instance):
        result = with_any(immutable_outer_instance, ("pair", 15))
        assert result._nodes_dict["pair"][0].value == 15


class TestWithAnyAllConstants:

    def test_multiple_constants_delegates_to_with_constants(self, immutable_outer_instance):
        result = with_any(
            immutable_outer_instance,
            (("first", 1), ("second", 2), ("third", 3)),
        )
        assert result._nodes_dict["first"][0].value == 1
        assert result._nodes_dict["second"][0].value == 2
        assert result._nodes_dict["third"][0].value == 3


class TestWithAnyMixedCompositeAndConstants:

    def test_composite_plus_unrelated_constant(self, immutable_outer_instance):
        result = with_any(
            immutable_outer_instance,
            (("pair", 20), ("third", 30)),
        )
        assert result._nodes_dict["pair"][0].value == 20
        assert result._nodes_dict["third"][0].value == 30
        assert result.value == 50

    def test_composite_plus_matching_contained_constant_succeeds(self, immutable_outer_instance):
        result = with_any(
            immutable_outer_instance,
            (("pair", 20), ("first", 20)),
        )
        assert result._nodes_dict["pair"][0].value == 20
        assert result._nodes_dict["first"][0].value == 20

    def test_composite_plus_conflicting_contained_constant_raises(self, immutable_outer_instance):
        changes = (("pair", 20), ("first", 999))
        with pytest.raises(Exception):
            with_any(
                immutable_outer_instance,
                changes,
            )


class TestWithAnyValidation:

    def test_changes_wrong_type_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_any(immutable_outer_instance, ["not", "a", "tuple"])

    def test_unknown_name_in_single_change_raises(self, immutable_outer_instance):
        with pytest.raises(Exception):
            with_any(immutable_outer_instance, ("nonexistent", 1))