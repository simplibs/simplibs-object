"""
Tests for `Unary` mixin.
"""
import pytest
from numbers import Number
from simplibs.object.mixins.core_mixins import NodesDicts, Snapshot
from simplibs.object.mixins.dunders.numeric import Unary
from simplibs.object.testing import assert_simple_mixin


class TestUnaryStructure:

    def test_only_types_is_number(self):
        assert Unary._only_types is Number

    def test_inherits_from_nodes_dicts_and_snapshot(self):
        assert issubclass(Unary, NodesDicts)
        assert issubclass(Unary, Snapshot)

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Unary,
            test_class=IntLeaf,
            method_names=("__neg__", "__pos__", "__abs__"),
        )


class TestUnaryOperatorsAtom:

    def test_neg(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = -instance
        assert result.value == -instance.value

    def test_pos(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = +instance
        assert result.value == +instance.value

    def test_abs(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = abs(instance)
        assert result.value == abs(instance.value)

    def test_operations_return_new_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = -instance
        assert result is not instance


class TestUnaryOperatorsComposite:

    def test_neg_on_composite(self, Outer):
        instance = Outer(mixins=(Unary,), mutable=False)
        result = -instance
        assert result.value == -instance.value