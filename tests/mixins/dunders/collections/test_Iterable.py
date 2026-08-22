"""
Tests for `Iterable` mixin.
"""
import pytest
from simplibs.object.mixins.dunders.collections import Iterable
from simplibs.object.testing import assert_simple_mixin


class TestIterableStructure:

    def test_composite_only_flag(self):
        assert Iterable._composite_only is True

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            Iterable,
            test_class=Outer,
            method_names=("__iter__", "__reversed__", "__dir__"),
        )


class TestIterableBehavior:

    def test_iter_yields_direct_inner_names(self, Outer):
        instance = Outer(mixins=(Iterable,))
        assert set(iter(instance)) == {"pair", "third"}

    def test_iter_order_matches_blueprint_order(self, Outer):
        instance = Outer(mixins=(Iterable,))
        assert list(instance) == ["pair", "third"]

    def test_reversed_yields_reverse_order(self, Outer):
        instance = Outer(mixins=(Iterable,))
        assert list(reversed(instance)) == ["third", "pair"]

    def test_dir_includes_inner_names(self, Outer):
        instance = Outer(mixins=(Iterable,))
        listing = dir(instance)
        assert "pair" in listing
        assert "third" in listing

    def test_dir_is_sorted_and_deduplicated(self, Outer):
        instance = Outer(mixins=(Iterable,))
        listing = dir(instance)
        assert listing == sorted(set(listing))


class TestIterableCompatibility:

    def test_rejects_atom_instance(self, IntLeaf):
        with pytest.raises(Exception):
            IntLeaf(mixins=(Iterable,), as_atom=True)