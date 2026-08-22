"""
Tests for `execute_inplace_op(self, operator, other)`.
"""
import operator as op
import pytest
from simplibs.object.mixins.dunders.numeric import Inplace
from simplibs.object.mixins.dunders.numeric._utils import execute_inplace_op


class TestExecuteInplaceOp:

    def test_addition_modifies_value_in_place(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        result = execute_inplace_op(instance, op.add, 5)
        assert result is instance
        assert instance.value == original + 5

    def test_other_as_instance_extracts_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        other = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        execute_inplace_op(instance, op.add, other)
        assert instance.value == original + other.value

    def test_incompatible_type_returns_not_implemented(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        result = execute_inplace_op(instance, op.add, "not_a_number")
        assert result is NotImplemented
        assert instance.value == original

    def test_zero_division_returns_not_implemented(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        result = execute_inplace_op(instance, op.truediv, 0)
        assert result is NotImplemented
        assert instance.value == original