"""
Tests for `testing/asserts/mixins/assert_mixins_slots_values.py`.
"""
import pytest
from simplibs.object.testing.asserts.mixins.assert_mixins_slots_values import (
    assert_mixins_slots_values,
)
from simplibs.object.testing.containers.TestMixin import TestMixin


class TestAssertMixinsSlotsValuesSingleTuple:

    def test_passes_for_single_key_value_tuple(self, IntConst, subtests):
        instance = IntConst(mixins=(TestMixin,))
        assert_mixins_slots_values(subtests, instance, ("_test_slot", "test_value"))


class TestAssertMixinsSlotsValuesSequence:

    def test_passes_for_sequence_of_pairs(self, IntConst, subtests):
        instance = IntConst(mixins=(TestMixin,))
        assert_mixins_slots_values(
            subtests,
            instance,
            (("_test_slot", "test_value"), ("test_property", "test_value")),
        )


class TestAssertMixinsSlotsValuesMismatch:

    def test_fails_when_value_does_not_match(self, IntConst, subtests):
        instance = IntConst(mixins=(TestMixin,))
        with pytest.raises(pytest.fail.Exception, match="has unexpected value"):
            assert_mixins_slots_values(
                subtests,
                instance,
                ("_test_slot", "wrong_value"),
                verbose=False,
            )

    def test_fails_when_slot_missing(self, IntConst, subtests):
        instance = IntConst(mixins=(TestMixin,))
        with pytest.raises(pytest.fail.Exception, match="does not contain expected slot"):
            assert_mixins_slots_values(
                subtests,
                instance,
                ("does_not_exist", "x"),
                verbose=False,
            )


class TestAssertMixinsSlotsValuesInputValidation:

    def test_invalid_top_level_structure_fails(self, IntConst, subtests):
        instance = IntConst(mixins=(TestMixin,))
        with pytest.raises(pytest.fail.Exception, match="must be a tuple"):
            assert_mixins_slots_values(
                subtests,
                instance,
                "not-a-tuple",
                verbose=False,
            )

    def test_non_string_slot_name_fails(self, IntConst, subtests):
        instance = IntConst(mixins=(TestMixin,))
        with pytest.raises(pytest.fail.Exception, match="is not a string identifier"):
            assert_mixins_slots_values(
                subtests,
                instance,
                ((123, "value"),),
                verbose=False,
            )