"""
Tests for `Ordering` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.comparison import Ordering
from simplibs.object.testing import assert_simple_mixin


class TestOrderingStructure:

    def test_slots_empty(self):
        assert Ordering.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            Ordering,
            test_class=IntLeaf,
            method_names=("__lt__", "__le__", "__gt__", "__ge__"),
        )


class TestOrderingComparisons:

    def test_lt_against_raw_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Ordering,), as_atom=True)
        assert instance < 100
        assert not (instance < 1)

    def test_le_against_raw_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Ordering,), as_atom=True)
        assert instance <= instance.value
        assert instance <= instance.value + 1

    def test_gt_against_raw_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Ordering,), as_atom=True)
        assert instance > 1
        assert not (instance > 100)

    def test_ge_against_raw_value(self, IntLeaf):
        instance = IntLeaf(mixins=(Ordering,), as_atom=True)
        assert instance >= instance.value
        assert instance >= instance.value - 1

    def test_comparison_between_two_instances(self, IntLeaf):
        a = IntLeaf(mixins=(Ordering,), as_atom=True)
        b = IntLeaf(mixins=(Ordering,), as_atom=True)
        assert (a < b) is False
        assert (a <= b) is True

    def test_incompatible_type_returns_not_implemented_leads_to_typeerror(self, IntLeaf):
        instance = IntLeaf(mixins=(Ordering,), as_atom=True)
        with pytest.raises(TypeError):
            _ = instance < "not_a_number"