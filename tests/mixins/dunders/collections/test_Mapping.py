"""
Tests for `Mapping` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.collections import Mapping
from simplibs.object.testing import assert_simple_mixin


class TestMappingStructure:

    def test_composite_only_flag(self):
        assert Mapping._composite_only is True

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Mapping,
            test_class=Outer,
            method_names=("__len__", "__contains__", "__getitem__", "get", "__setitem__"),
        )


class TestMappingLenContains:

    def test_len_equals_direct_inners_count(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert len(instance) == 2  # pair, third

    def test_contains_true_for_existing_key(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert "third" in instance

    def test_contains_false_for_nested_key(self, Outer):
        """'first' is nested under 'pair', not a direct inner of Outer."""
        instance = Outer(mixins=(Mapping,))
        assert "first" not in instance

    def test_contains_false_for_unknown_key(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert "nonexistent" not in instance


class TestMappingGetitem:

    def test_getitem_returns_value(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert instance["third"] == 3

    def test_getitem_unknown_key_raises_keyerror(self, Outer):
        instance = Outer(mixins=(Mapping,))
        with pytest.raises(KeyError):
            _ = instance["nonexistent"]

    def test_get_returns_default_for_unknown_key(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert instance.get("nonexistent", "fallback") == "fallback"

    def test_get_returns_none_default(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert instance.get("nonexistent") is None

    def test_get_returns_value_for_existing_key(self, Outer):
        instance = Outer(mixins=(Mapping,))
        assert instance.get("third") == 3


class TestMappingSetitem:

    def test_setitem_updates_value_on_mutable_instance(self, Outer):
        instance = Outer(mixins=(Mapping,), mutable=True)
        instance["third"] = 99
        assert instance["third"] == 99

    def test_setitem_unknown_key_raises_keyerror(self, Outer):
        instance = Outer(mixins=(Mapping,), mutable=True)
        with pytest.raises(KeyError):
            instance["nonexistent"] = 1

    def test_setitem_on_immutable_instance_raises_typeerror(self, Outer):
        instance = Outer(mixins=(Mapping,), mutable=False)
        with pytest.raises(TypeError):
            instance["third"] = 99


class TestMappingCompatibility:

    def test_rejects_atom_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(Mapping,), as_atom=True)