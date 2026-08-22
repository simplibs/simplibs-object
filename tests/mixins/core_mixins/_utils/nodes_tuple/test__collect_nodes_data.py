"""
Tests for `_collect_nodes_data(instance, path, nodes_list)`.
"""
from simplibs.object.mixins._common_logic.constants import VALUE
from simplibs.object.mixins.core_mixins._utils.nodes_tuple._collect_nodes_data import (
    _collect_nodes_data,
)


class TestCollectNodesDataAtom:

    def test_atom_appends_single_entry(self, IntLeaf):
        instance = IntLeaf()
        nodes_list = []
        _collect_nodes_data(instance, (), nodes_list)
        assert len(nodes_list) == 1
        assert nodes_list[0] == (instance, ())

    def test_atom_returns_immediately_no_recursion(self, IntLeaf):
        instance = IntLeaf()
        nodes_list = []
        _collect_nodes_data(instance, ("prefix",), nodes_list)
        assert nodes_list == [(instance, ("prefix",))]


class TestCollectNodesDataComposite:

    def test_composite_root_gets_value_suffix(self, Outer):
        instance = Outer()
        nodes_list = []
        _collect_nodes_data(instance, (), nodes_list)

        # Root instance (Outer) must have path == (VALUE,)
        root_entries = [entry for entry in nodes_list if entry[0] is instance]
        assert len(root_entries) == 1
        assert root_entries[0][1] == (VALUE,)

    def test_all_leaves_present(self, Outer):
        instance = Outer()
        nodes_list = []
        _collect_nodes_data(instance, (), nodes_list)

        paths = {entry[1] for entry in nodes_list}
        expected_paths = {
            (VALUE,),
            ("pair", VALUE),
            ("pair", "first"),
            ("pair", "second"),
            ("third",),
        }
        assert expected_paths <= paths

    def test_nested_composite_gets_value_suffix_on_its_own_path(self, Outer):
        instance = Outer()
        nodes_list = []
        _collect_nodes_data(instance, (), nodes_list)

        pair_instance = instance._pair
        pair_entries = [
            entry for entry in nodes_list
            if entry[0] is pair_instance
        ]
        assert len(pair_entries) == 1
        _, pair_path = pair_entries[0]
        assert pair_path == ("pair", VALUE)

    def test_leaf_inside_composite_has_full_path(self, Outer):
        instance = Outer()
        nodes_list = []
        _collect_nodes_data(instance, (), nodes_list)

        first_instance = instance._pair._first
        first_entries = [
            entry for entry in nodes_list
            if entry[0] is first_instance
        ]
        assert len(first_entries) == 1
        _, first_path = first_entries[0]
        assert first_path == ("pair", "first")

    def test_total_node_count(self, Outer):
        """5 nodes: outer(composite), pair(composite), first, second, third."""
        instance = Outer()
        nodes_list = []
        _collect_nodes_data(instance, (), nodes_list)
        assert len(nodes_list) == 5