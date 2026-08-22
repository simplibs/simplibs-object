"""
Tests for `CollectionBase` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.collections import CollectionBase
from simplibs.object.testing import assert_simple_mixin


class TestCollectionBaseStructure:

    def test_composite_only_flag(self):
        assert CollectionBase._composite_only is True

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            CollectionBase,
            test_class=Outer,
            slots_names=("_inners_name_set", "_inners_name_tuple"),
            method_names=("keys", "values", "items"),
        )


class TestCollectionBaseDirectInnersOnly:

    def test_keys_are_only_direct_inners(self, Outer):
        """
        Outer._inners = (Pair, Third) - so keys() should contain
        'pair' and 'third', NOT 'first'/'second' (which are nested deeper).
        """
        instance = Outer(mixins=(CollectionBase,))
        assert set(instance.keys()) == {"pair", "third"}

    def test_values_correspond_to_keys_order(self, Outer):
        instance = Outer(mixins=(CollectionBase,))
        keys = instance.keys()
        values = instance.values()
        assert len(keys) == len(values)

    def test_items_pairs_keys_with_values(self, Outer):
        instance = Outer(mixins=(CollectionBase,))
        items = instance.items()
        assert set(k for k, _ in items) == set(instance.keys())


class TestCollectionBaseCompatibility:

    def test_rejects_atom_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(CollectionBase,), as_atom=True)