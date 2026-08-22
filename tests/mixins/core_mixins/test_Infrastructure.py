"""
Tests for `Infrastructure` mixin.
"""
from simplibs.object.mixins.core_mixins import Infrastructure, NodesDicts, Snapshot
from simplibs.object.testing import assert_simple_mixin


class TestInfrastructureStructure:

    def test_inherits_from_nodes_dicts_and_snapshot(self):
        assert issubclass(Infrastructure, NodesDicts)
        assert issubclass(Infrastructure, Snapshot)

    def test_slots_empty(self):
        assert Infrastructure.__slots__ == ()

    def test_assert_simple_mixin_shallow(self, subtests, Outer):
        assert_simple_mixin(subtests, Infrastructure, test_class=Outer)


class TestInfrastructureCombinedBehavior:

    def test_provides_both_apis(self, Outer):
        instance = Outer(mixins=(Infrastructure,))

        # From Snapshot
        assert hasattr(instance, "_build_snapshot")
        assert hasattr(instance, "_restore_snapshot")
        assert hasattr(instance, "_compare_snapshots")

        # From NodesDicts
        assert hasattr(instance, "_nodes_dict")
        assert hasattr(instance, "_nodes_instance_dict")
        assert hasattr(instance, "_nodes_path_dict")
        assert hasattr(instance, "_nodes_index_map")

        # From NodesTuple
        assert hasattr(instance, "_nodes_tuple")

    def test_snapshot_and_nodes_dict_reference_same_nodes_tuple(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        snapshot = instance._build_snapshot()
        assert len(snapshot) == len(instance._nodes_dict)

    def test_no_slot_conflict_on_instantiation(self, Outer):
        instance = Outer(mixins=(Infrastructure,))
        assert instance is not None