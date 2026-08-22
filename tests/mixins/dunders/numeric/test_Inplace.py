"""
Tests for `Inplace` mixin.
"""
import pytest
from numbers import Number
from simplibs.object.mixins.dunders.numeric import Inplace
from simplibs.object.testing import assert_simple_mixin


class TestInplaceStructure:

    def test_mutable_only_flag(self):
        assert Inplace._mutable_only is True

    def test_only_types_is_number(self):
        assert Inplace._only_types is Number

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Inplace,
            test_class=IntLeaf,
            method_names=(
                "__iadd__",
                "__isub__",
                "__imul__",
                "__itruediv__",
                "__ifloordiv__",
                "__imod__",
                "__ipow__",
            ),
        )


class TestInplaceOperators:

    def test_iadd_modifies_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        instance += 5
        assert instance.value == original + 5

    def test_isub_modifies_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        instance -= 2
        assert instance.value == original - 2

    def test_imul_modifies_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        instance *= 3
        assert instance.value == original * 3

    def test_ipow_modifies_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        original = instance.value
        instance **= 2
        assert instance.value == original**2

    def test_iadd_returns_same_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Inplace,), as_atom=True, mutable=True)
        result = instance.__iadd__(1)
        assert result is instance


class TestInplaceCompatibility:

    def test_rejects_immutable_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(Inplace,), as_atom=True, mutable=False)