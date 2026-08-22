"""
Tests for `Bitwise` mixin.
"""
import pytest
from numbers import Integral
from simplibs.object.mixins.dunders.numeric import Bitwise
from simplibs.object.testing import assert_simple_mixin


class TestBitwiseStructure:

    def test_constant_only_flag(self):
        assert Bitwise._constant_only is True

    def test_only_types_is_integral(self):
        assert Bitwise._only_types is Integral

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Bitwise,
            test_class=IntLeaf,
            method_names=(
                "__and__",
                "__rand__",
                "__or__",
                "__ror__",
                "__xor__",
                "__rxor__",
                "__lshift__",
                "__rlshift__",
                "__rshift__",
                "__rrshift__",
                "__invert__",
            ),
        )


class TestBitwiseOperators:

    def test_and(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = instance & 3
        assert result.value == (instance.value & 3)

    def test_or(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = instance | 8
        assert result.value == (instance.value | 8)

    def test_xor(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = instance ^ 5
        assert result.value == (instance.value ^ 5)

    def test_lshift(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = instance << 2
        assert result.value == (instance.value << 2)

    def test_rshift(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = instance >> 1
        assert result.value == (instance.value >> 1)

    def test_invert(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = ~instance
        assert result.value == ~instance.value

    def test_operations_return_new_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Bitwise,), as_atom=True, mutable=False)
        result = instance | 0
        assert result is not instance


class TestBitwiseCompatibility:

    def test_rejects_composite_instance(self, Outer):
        with pytest.raises(Exception):
            Outer(mixins=(Bitwise,))

    def test_rejects_float_type(self):
        from simplibs.object import SimpleConstant

        class FloatLeaf(SimpleConstant):
            _type = float
            _default = 1.5

        with pytest.raises(Exception):
            FloatLeaf(mixins=(Bitwise,), as_atom=True)