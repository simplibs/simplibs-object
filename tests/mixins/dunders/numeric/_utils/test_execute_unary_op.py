"""
Tests for `execute_unary_op(self, operator)`.
"""
import operator as op
from simplibs.object.mixins.dunders.numeric import Unary
from simplibs.object.mixins.dunders.numeric._utils import execute_unary_op


class TestExecuteUnaryOp:

    def test_negation_returns_new_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = execute_unary_op(instance, op.neg)
        assert result is not instance
        assert result.value == -instance.value

    def test_positive_returns_equivalent_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = execute_unary_op(instance, op.pos)
        assert result.value == +instance.value

    def test_abs_operation(self, IntLeaf):
        instance = IntLeaf(mixins=(Unary,), as_atom=True, mutable=False)
        result = execute_unary_op(instance, abs)
        assert result.value == abs(instance.value)

    def test_works_on_composite_root(self, Outer):
        instance = Outer(mixins=(Unary,), mutable=False)
        result = execute_unary_op(instance, op.neg)
        assert result.value == -instance.value