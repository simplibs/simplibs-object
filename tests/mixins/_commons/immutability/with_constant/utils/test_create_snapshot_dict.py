"""
Tests for `create_snapshot_dict(nodes_tuple)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_constant.utils import (
    create_snapshot_dict,
)


class TestCreateSnapshotDict:

    def test_returns_dict(self, immutable_outer_instance):
        result = create_snapshot_dict(immutable_outer_instance._nodes_tuple)
        assert isinstance(result, dict)

    def test_keys_match_node_names(self, immutable_outer_instance):
        result = create_snapshot_dict(immutable_outer_instance._nodes_tuple)
        assert set(result.keys()) == set(immutable_outer_instance._node_names_tuple)

    def test_values_match_current_node_values(self, immutable_outer_instance):
        result = create_snapshot_dict(immutable_outer_instance._nodes_tuple)
        for instance, _ in immutable_outer_instance._nodes_tuple:
            assert result[instance.meta.name_snake] == instance.value

    def test_contains_leaf_and_composite_names(self, immutable_outer_instance):
        result = create_snapshot_dict(immutable_outer_instance._nodes_tuple)
        # Must contain keys for all tree nodes (leaves and composites)
        for instance, _ in immutable_outer_instance._nodes_tuple:
            assert instance.meta.name_snake in result