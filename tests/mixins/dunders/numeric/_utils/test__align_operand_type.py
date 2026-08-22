"""
Tests for `_align_operand_type(self, value)`.
"""
from simplibs.object.mixins.dunders.numeric._utils._align_operand_type import (
    _align_operand_type,
)


class TestAlignOperandType:

    def test_int_to_float_conversion(self, IntLeaf):
        instance = IntLeaf(as_atom=True)
        result = _align_operand_type(instance, 5.0)
        assert result == 5
        assert isinstance(result, int)

    def test_safe_conversion_with_float_target(self):
        from simplibs.object import SimpleConstant

        class FloatLeaf(SimpleConstant):
            _type = float
            _default = 1.0

        instance = FloatLeaf(as_atom=True)
        result = _align_operand_type(instance, 5)
        assert result == 5.0
        assert isinstance(result, float)

    def test_unconvertible_value_returned_unchanged(self, IntLeaf):
        instance = IntLeaf(as_atom=True)
        result = _align_operand_type(instance, "not_a_number")
        assert result == "not_a_number"

    def test_none_returned_unchanged_if_unconvertible(self, IntLeaf):
        instance = IntLeaf(as_atom=True)
        result = _align_operand_type(instance, None)
        assert result is None