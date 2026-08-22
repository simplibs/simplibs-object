"""
Tests for `NodesDicts` mixin.
"""
from types import MappingProxyType
import pytest
from simplibs.object.mixins.core_mixins import NodesDicts
from simplibs.object.testing import assert_simple_mixin


class TestNodesDictsStructure:

    def test_slots_present(self, subtests, Outer):
        assert_simple_mixin(
            subtests,
            NodesDicts,
            test_class=Outer,
            slots_names=(
                "_nodes_dict",
                "_nodes_instance_dict",
                "_nodes_path_dict",
                "_nodes_index_map",
            ),
        )

    def test_all_dicts_are_mapping_proxy(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        assert isinstance(instance._nodes_dict, MappingProxyType)
        assert isinstance(instance._nodes_instance_dict, MappingProxyType)
        assert isinstance(instance._nodes_path_dict, MappingProxyType)
        assert isinstance(instance._nodes_index_map, MappingProxyType)

    def test_dicts_are_immutable(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        with pytest.raises(TypeError):
            instance._nodes_dict["new_key"] = "value"


class TestNodesDictsContent:

    def test_nodes_dict_maps_name_to_instance_and_path(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        node_instance, node_path = instance._nodes_dict["third"]
        assert node_instance.meta.name_snake == "third"
        assert node_path == ("third",)

    def test_nodes_instance_dict_maps_name_to_instance(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        third_instance = instance._nodes_instance_dict["third"]
        assert third_instance.meta.name_snake == "third"

    def test_nodes_path_dict_maps_name_to_path(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        assert instance._nodes_path_dict["first"] == ("pair", "first")

    def test_nodes_index_map_maps_name_to_index(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        for name, index in instance._nodes_index_map.items():
            assert instance._nodes_tuple[index][0].meta.name_snake == name

    def test_all_dicts_have_same_keys(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        keys = set(instance._nodes_dict.keys())
        assert set(instance._nodes_instance_dict.keys()) == keys
        assert set(instance._nodes_path_dict.keys()) == keys
        assert set(instance._nodes_index_map.keys()) == keys

    def test_dict_keys_match_node_names_tuple(self, Outer):
        instance = Outer(mixins=(NodesDicts,))
        assert set(instance._nodes_dict.keys()) == set(instance._node_names_tuple)