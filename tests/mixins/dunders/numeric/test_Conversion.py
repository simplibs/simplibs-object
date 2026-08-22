"""
Tests for `Conversion` mixin.
"""
import math
import pytest
from numbers import Number
from simplibs.object.mixins.dunders.numeric import Conversion
from simplibs.object.testing import assert_simple_mixin


class TestConversionStructure:

    def test_only_types_is_number(self):
        assert Conversion._only_types is Number

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Conversion,
            test_class=IntLeaf,
            method_names=(
                "__int__",
                "__float__",
                "__complex__",
                "__index__",
                "__round__",
                "__floor__",
                "__ceil__",
                "__trunc__",
            ),
        )


class TestConversionNativeTypes:

    def test_int_conversion(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        result = int(instance)
        assert result == instance.value
        assert type(result) is int

    def test_float_conversion(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        result = float(instance)
        assert type(result) is float

    def test_complex_conversion(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        result = complex(instance)
        assert type(result) is complex

    def test_round_conversion(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        assert round(instance) == round(instance.value)

    def test_round_with_ndigits(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        assert round(instance, 2) == round(instance.value, 2)

    def test_floor_ceil_trunc(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        assert math.floor(instance) == math.floor(instance.value)
        assert math.ceil(instance) == math.ceil(instance.value)
        assert math.trunc(instance) == math.trunc(instance.value)


class TestConversionIndex:

    def test_index_returns_int_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        assert instance.__index__() == instance.value

    def test_index_usable_in_slicing(self, IntLeaf):
        instance = IntLeaf(mixins=(Conversion,), as_atom=True)
        my_list = list(range(20))
        assert my_list[instance] == my_list[instance.value]

    def test_index_raises_for_non_int_value(self):
        from simplibs.object import SimpleConstant

        class FloatLeaf(SimpleConstant):
            _type = float
            _default = 1.5

        instance = FloatLeaf(mixins=(Conversion,), as_atom=True)
        with pytest.raises(TypeError):
            instance.__index__()