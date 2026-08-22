"""
Tests for `Arithmetic` mixin.
"""
import pytest
from numbers import Number
from simplibs.object.mixins.core_mixins import NodesDicts, Snapshot
from simplibs.object.mixins.dunders.numeric import Arithmetic
from simplibs.object.testing import assert_simple_mixin


class TestArithmeticStructure:

    def test_only_types_is_number(self):
        assert Arithmetic._only_types is Number

    def test_inherits_from_nodes_dicts_and_snapshot(self):
        assert issubclass(Arithmetic, NodesDicts)
        assert issubclass(Arithmetic, Snapshot)

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Arithmetic,
            test_class=IntLeaf,
            method_names=(
                "__add__",
                "__radd__",
                "__sub__",
                "__rsub__",
                "__mul__",
                "__rmul__",
                "__truediv__",
                "__rtruediv__",
                "__floordiv__",
                "__rfloordiv__",
                "__mod__",
                "__rmod__",
                "__pow__",
                "__rpow__",
            ),
        )


class TestArithmeticOperatorsAtom:

    def test_add(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance + 3
        assert result.value == instance.value + 3

    def test_radd(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = 10 + instance
        assert result.value == 10 + instance.value

    def test_sub(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance - 2
        assert result.value == instance.value - 2

    def test_mul(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance * 2
        assert result.value == instance.value * 2

    def test_floordiv(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance // 2
        assert result.value == instance.value // 2
        assert isinstance(result, type(instance))

    def test_truediv(self, FloatLeaf):
        instance = FloatLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance / 2
        assert result.value == instance.value / 2
        assert isinstance(result, type(instance))

    def test_pow(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance**2
        assert result.value == instance.value**2

    def test_operations_return_new_instance(self, IntLeaf):
        instance = IntLeaf(mixins=(Arithmetic,), as_atom=True, mutable=False)
        result = instance + 1
        assert result is not instance


class TestArithmeticOperatorsComposite:

    def test_add_on_composite(self, Outer):
        instance = Outer(mixins=(Arithmetic,), mutable=False)
        result = instance + 100
        assert result.value == instance.value + 100