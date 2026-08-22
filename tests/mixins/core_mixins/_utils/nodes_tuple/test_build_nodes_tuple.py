"""
Tests for `build_nodes_tuple(self)`.
"""
from simplibs.object.mixins.core_mixins._utils.nodes_tuple import build_nodes_tuple


class TestBuildNodesTuple:

    def test_returns_tuple(self, IntLeaf):
        instance = IntLeaf()
        result = build_nodes_tuple(instance)
        assert isinstance(result, tuple)

    def test_atom_single_entry(self, IntLeaf):
        instance = IntLeaf()
        result = build_nodes_tuple(instance)
        assert result == ((instance, ()),)

    def test_composite_matches_manual_collection(self, Outer):
        from simplibs.object.mixins.core_mixins._utils.nodes_tuple._collect_nodes_data import (
            _collect_nodes_data,
        )

        instance = Outer()
        manual_list = []
        _collect_nodes_data(instance, (), manual_list)

        result = build_nodes_tuple(instance)

        assert result == tuple(manual_list)

    def test_composite_has_five_nodes(self, Outer):
        instance = Outer()
        result = build_nodes_tuple(instance)
        assert len(result) == 5