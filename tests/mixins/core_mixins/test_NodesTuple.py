"""
Tests for `NodesTuple` mixin.
"""
from simplibs.object.mixins.core_mixins import NodesTuple
from simplibs.object.testing import assert_simple_mixin


class TestNodesTupleStructure:

    def test_slots_present_on_atom(self, subtests, IntLeaf):
        assert_simple_mixin(
            subtests,
            NodesTuple,
            test_class=IntLeaf,
            slots_names=("_nodes_tuple", "_node_names_tuple", "_constant_names_set"),
        )

    def test_slots_present_on_composite(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            NodesTuple,
            test_class=Outer,
            slots_names=("_nodes_tuple", "_node_names_tuple", "_constant_names_set"),
        )


class TestNodesTupleBehaviorAtom:

    def test_nodes_tuple_has_single_entry(self, IntLeaf):
        instance = IntLeaf(mixins=(NodesTuple,))
        assert len(instance._nodes_tuple) == 1

    def test_node_names_tuple_contains_own_name(self, IntLeaf):
        instance = IntLeaf(mixins=(NodesTuple,))
        assert instance._node_names_tuple == (instance.meta.name_snake,)

    def test_constant_names_set_contains_self(self, IntLeaf):
        instance = IntLeaf(mixins=(NodesTuple,))
        assert instance._constant_names_set == {instance.meta.name_snake}


class TestNodesTupleBehaviorComposite:

    def test_nodes_tuple_has_five_entries(self, Outer):
        instance = Outer(mixins=(NodesTuple,))
        assert len(instance._nodes_tuple) == 5

    def test_node_names_tuple_contains_all_names(self, Outer):
        instance = Outer(mixins=(NodesTuple,))
        expected_names = {
            instance.meta.name_snake,
            instance._pair.meta.name_snake,
            instance._pair._first.meta.name_snake,
            instance._pair._second.meta.name_snake,
            instance._third.meta.name_snake,
        }
        assert set(instance._node_names_tuple) == expected_names

    def test_constant_names_set_excludes_composites(self, Outer):
        instance = Outer(mixins=(NodesTuple,))
        expected_constants = {
            instance._pair._first.meta.name_snake,
            instance._pair._second.meta.name_snake,
            instance._third.meta.name_snake,
        }
        assert instance._constant_names_set == expected_constants
        assert instance._pair.meta.name_snake not in instance._constant_names_set
        assert instance.meta.name_snake not in instance._constant_names_set