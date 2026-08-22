"""
Tests for `testing/containers/InnerValue.py`.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.object.testing.containers.InnerValue import InnerValue


class TestInnerValuePathNormalization:

    def test_dot_separated_string_path_is_split(self):
        iv = InnerValue(path="address.city.zip", value=1)
        assert iv.path == ("address", "city", "zip")

    def test_single_segment_string_path(self):
        iv = InnerValue(path="first", value=1)
        assert iv.path == ("first",)

    def test_iterable_of_strings_is_converted_to_tuple(self):
        iv = InnerValue(path=("address", "city"), value=1)
        assert iv.path == ("address", "city")

    def test_list_path_is_converted_to_tuple(self):
        iv = InnerValue(path=["a", "b"], value=1)
        assert iv.path == ("a", "b")


class TestInnerValuePathValidation:

    def test_empty_tuple_path_raises(self):
        with pytest.raises(SimpleRuntimeError):
            InnerValue(path=(), value=1)

    def test_empty_string_path_does_not_raise_but_yields_single_empty_segment(self):
        iv = InnerValue(path="", value=1)
        assert iv.path == ("",)

    def test_non_string_item_in_path_raises(self):
        with pytest.raises(SimpleRuntimeError):
            InnerValue(path=("first", 2), value=1)


class TestInnerValueIsFrozen:

    def test_path_cannot_be_reassigned_after_init(self):
        iv = InnerValue(path="first", value=1)
        with pytest.raises(Exception):
            iv.path = "second"

    def test_value_cannot_be_reassigned_after_init(self):
        iv = InnerValue(path="first", value=1)
        with pytest.raises(Exception):
            iv.value = 2


class TestInnerValueAsInstanceTuple:

    def test_single_level_path_resolves_inner_instance(self, NonDecomposablePairObject):
        instance = NonDecomposablePairObject(mixins=())
        iv = InnerValue(path="first", value=99)

        target, value = iv.as_instance_tuple(instance)
        assert target is instance.first_instance
        assert value == 99

    def test_missing_property_returns_unset(self, NonDecomposablePairObject):
        instance = NonDecomposablePairObject(mixins=())
        iv = InnerValue(path="does_not_exist", value=1)

        assert iv.as_instance_tuple(instance) is UNSET

    def test_none_intermediate_returns_unset(self, NonDecomposablePairObject):
        instance = NonDecomposablePairObject(mixins=())

        class FakeWithNoneInstance:
            first_instance = None

        iv = InnerValue(path="first", value=1)
        assert iv.as_instance_tuple(FakeWithNoneInstance()) is UNSET