"""
Tests for `execute_arithmetic_op(self, operator, other, *, is_reversed=False)`.
"""
import operator as op
import pytest
from simplibs.object.mixins.dunders.numeric import Arithmetic
from simplibs.object.mixins.dunders.numeric._utils import execute_arithmetic_op


class TestExecuteArithmeticOpAtom:

    def test_simple_addition_returns_new_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = execute_arithmetic_op(instance, op.add, 5)
        assert result is not instance
        assert result.value == instance.value + 5

    def test_other_as_instance_extracts_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        other = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = execute_arithmetic_op(instance, op.add, other)
        assert result.value == instance.value + other.value

    def test_is_reversed_flips_operand_order(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = execute_arithmetic_op(instance, op.sub, 100, is_reversed=True)
        assert result.value == 100 - instance.value


class TestExecuteArithmeticOpComposite:

    def test_addition_on_composite_root(self, Outer):
        instance = Outer(mixins=(Arithmetic,), mutable=False)
        original = instance.value
        result = execute_arithmetic_op(instance, op.add, 10)
        assert result.value == original + 10


class TestExecuteArithmeticOpFallback:

    def test_incompatible_type_returns_not_implemented(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = execute_arithmetic_op(instance, op.add, "not_a_number")
        assert result is NotImplemented

    def test_safe_type_alignment_recovers_operation(self):
        from simplibs.object import SimpleConstant

        class FloatLeaf(SimpleConstant):
            _type = float
            _default = 1.5

        instance = FloatLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = execute_arithmetic_op(instance, op.add, 1)
        assert result.value == 2.5