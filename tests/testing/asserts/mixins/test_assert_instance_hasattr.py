"""
Tests for `testing/asserts/mixins/assert_instance_hasattr.py`.
"""
import pytest
from simplibs.object.testing.asserts.mixins.assert_instance_hasattr import (
    assert_instance_hasattr,
)


class TestAssertInstanceHasattrHappyPath:

    def test_passes_when_all_attributes_present(self, IntConst, subtests):
        instance = IntConst()
        assert_instance_hasattr(subtests, instance, names=("value",), kind="property")

    def test_multiple_names(self, IntConst, subtests):
        instance = IntConst()
        assert_instance_hasattr(
            subtests, instance, names=("value", "meta"), kind="attribute"
        )


class TestAssertInstanceHasattrMissing:

    def test_fails_when_attribute_missing(self, IntConst, subtests):
        instance = IntConst()
        with pytest.raises(pytest.fail.Exception, match="is missing expected slot 'does_not_exist'"):
            assert_instance_hasattr(
                subtests,
                instance,
                names=("does_not_exist",),
                kind="slot",
                verbose=False,
            )


class TestAssertInstanceHasattrInputValidation:

    def test_non_tuple_names_fails(self, IntConst, subtests):
        instance = IntConst()
        with pytest.raises(pytest.fail.Exception, match="must be a tuple of strings"):
            assert_instance_hasattr(
                subtests,
                instance,
                names=["value"],  # type: ignore[arg-type]
                kind="attribute",
                verbose=False,
            )

    def test_non_string_name_in_tuple_fails(self, IntConst, subtests):
        instance = IntConst()
        with pytest.raises(pytest.fail.Exception, match="is not a string"):
            assert_instance_hasattr(
                subtests,
                instance,
                names=(123,),  # type: ignore[arg-type]
                kind="attribute",
                verbose=False,
            )