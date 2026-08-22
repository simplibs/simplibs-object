"""
Tests for `InnersProperty` mixin.
"""
import pytest
from simplibs.object.mixins.others.properties import InnersProperty
from simplibs.object.mixins.others.properties._inners_property_utils import (
    collect_all_nested_properties,
)
from simplibs.object.testing import assert_simple_mixin


class TestInnersPropertyStructure:

    def test_composite_only_flag(self):
        assert InnersProperty._composite_only is True

    def test_slots_empty(self):
        assert InnersProperty.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(subtests, InnersProperty, test_class=Outer)


class TestInnersPropertyExtendInstanceClass:

    def test_nested_properties_attached_to_instance_class(self, Outer):
        instance = Outer(mixins=(InnersProperty,))
        expected_props = collect_all_nested_properties(Outer.meta)

        for name in expected_props:
            assert hasattr(type(instance), name)
            assert isinstance(getattr(type(instance), name), property)

    def test_composite_without_nested_inners_adds_no_properties(self, PairObject):
        instance = PairObject(mixins=(InnersProperty,))
        expected_props = collect_all_nested_properties(PairObject.meta)
        assert expected_props == {}


class TestInnersPropertyCompatibility:

    def test_rejects_atom_only_test_class(self, subtests, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(InnersProperty,), as_atom=True)