"""
Tests for `ValueDisplay` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.representation import ValueDisplay
from simplibs.object.testing import assert_simple_mixin


class TestValueDisplayStructure:

    def test_constant_only_flag(self):
        assert ValueDisplay._constant_only is True

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            ValueDisplay,
            test_class=IntLeaf,
            method_names=("__repr__", "__str__"),
        )


class TestValueDisplayRepr:

    def test_repr_format(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueDisplay,), as_atom=True)
        assert repr(instance) == f"{instance.meta.class_name}({instance.value!r})"

    def test_repr_contains_class_name(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueDisplay,), as_atom=True)
        assert instance.meta.class_name in repr(instance)


class TestValueDisplayStr:

    def test_str_returns_plain_value_string(self, IntLeaf):
        instance = IntLeaf(mixins=(ValueDisplay,), as_atom=True)
        assert str(instance) == str(instance.value)


class TestValueDisplayCompatibility:

    def test_rejects_composite_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(ValueDisplay,))