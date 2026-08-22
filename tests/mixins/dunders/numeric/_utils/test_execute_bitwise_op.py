"""
Tests for `execute_bitwise_op(self, operator, other, is_reversed=False)`.
"""
import operator as op
from simplibs.object.mixins.dunders.numeric import Bitwise
from simplibs.object.mixins.dunders.numeric._utils import execute_bitwise_op


class TestExecuteBitwiseOp:

    def test_and_operation(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = execute_bitwise_op(instance, op.and_, 3)
        assert result.value == (instance.value & 3)

    def test_or_operation(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = execute_bitwise_op(instance, op.or_, 8)
        assert result.value == (instance.value | 8)

    def test_is_reversed_flips_operand_order(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = execute_bitwise_op(instance, op.lshift, 2, is_reversed=True)
        assert result.value == (2 << instance.value)

    def test_incompatible_type_returns_not_implemented(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = execute_bitwise_op(instance, op.and_, "not_an_int")
        assert result is NotImplemented

    def test_returns_new_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = execute_bitwise_op(instance, op.or_, 1)
        assert result is not instance