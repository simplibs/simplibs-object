"""
Tests for `Collection` bundle mixin - `Iterable + Mapping` combined.
"""
import pytest
from simplibs.object.mixins.dunders.collections import Iterable, Mapping
from simplibs.object.mixins.dunders.collections.main import Collection
from simplibs.object.testing import assert_simple_mixin


class TestCollectionStructure:

    def test_composite_only_flag(self):
        assert Collection._composite_only is True

    def test_inherits_from_iterable_and_mapping(self):
        assert issubclass(Collection, Iterable)
        assert issubclass(Collection, Mapping)

    def test_slots_empty(self):
        assert Collection.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(subtests, Collection, test_class=Outer)


class TestCollectionCombinedAPI:

    def test_provides_both_iterable_and_mapping_api(self, Outer):
        instance = Outer(mixins=(Collection,))
        # Iterable
        assert list(instance) == ["pair", "third"]
        # Mapping
        assert instance["third"] == 3
        assert len(instance) == 2

    def test_no_slot_conflict_on_instantiation(self, Outer):
        instance = Outer(mixins=(Collection,))
        assert instance is not None


class TestCollectionCompatibility:

    def test_rejects_atom_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(Collection,), as_atom=True)