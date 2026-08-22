"""
Tests for `Equality` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.comparison import Equality
from simplibs.object.testing import assert_simple_mixin


class TestEqualityStructure:

    def test_slots_empty(self):
        assert Equality.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Equality,
            test_class=Outer,
            method_names=("__eq__", "__hash__"),
        )


class TestEqualityEqOperator:

    def test_equal_to_raw_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Equality,), as_atom=True)
        assert instance == instance.value

    def test_not_equal_to_different_raw_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Equality,), as_atom=True)
        assert instance != (instance.value + 1)

    def test_equal_to_same_blueprint_same_value(self, IntLeaf):
        a = IntLeaf(mixins=(Equality,), as_atom=True)
        b = IntLeaf(mixins=(Equality,), as_atom=True)
        assert a == b

    def test_different_blueprint_not_equal_even_with_same_value(self, Outer, IntLeaf):
        instance = Outer(mixins=(Equality,))
        other = IntLeaf(mixins=(Equality,), as_atom=True)
        assert instance != other


class TestEqualityHash:

    def test_mutable_instance_uses_identity_hash(self, IntLeaf):
        instance = IntLeaf(mixins=(Equality,), as_atom=True, mutable=True)
        assert hash(instance) == id(instance)

    def test_immutable_instance_uses_value_hash(self, IntLeaf):
        instance = IntLeaf(mixins=(Equality,), as_atom=True, mutable=False)
        assert hash(instance) == hash(instance.value)

    def test_two_equal_immutable_instances_have_same_hash(self, IntLeaf):
        a = IntLeaf(mixins=(Equality,), as_atom=True, mutable=False)
        b = IntLeaf(mixins=(Equality,), as_atom=True, mutable=False)
        assert hash(a) == hash(b)

    def test_two_mutable_instances_have_different_hash(self, IntLeaf):
        a = IntLeaf(mixins=(Equality,), as_atom=True, mutable=True)
        b = IntLeaf(mixins=(Equality,), as_atom=True, mutable=True)
        assert hash(a) != hash(b)