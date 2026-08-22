"""
Tests for `reacalculate_owner_value(snapshot_dict, owner)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_constant.utils import (
    create_snapshot_dict,
    reacalculate_owner_value,
)


class TestReacalculateOwnerValue:

    def test_updates_owner_entry_in_snapshot_dict(self, immutable_outer_instance):
        pair_instance = immutable_outer_instance._nodes_dict["pair"][0]
        snapshot_dict = create_snapshot_dict(immutable_outer_instance._nodes_tuple)

        # Simulate modifying 'first' directly in snapshot_dict
        snapshot_dict["first"] = 50

        reacalculate_owner_value(snapshot_dict, pair_instance)

        # pair = first(50) + second(2) = 52
        assert snapshot_dict["pair"] == 52
        # outer = pair(52) + third(3) = 55 (verifies root propagation)
        assert snapshot_dict["outer"] == 55

    def test_uses_correct_logic_function(self, immutable_outer_instance):
        pair_instance = immutable_outer_instance._nodes_dict["pair"][0]
        snapshot_dict = create_snapshot_dict(immutable_outer_instance._nodes_tuple)
        original_pair_value = snapshot_dict["pair"]
        original_outer_value = snapshot_dict["outer"]

        reacalculate_owner_value(snapshot_dict, pair_instance)

        # Without inner changes, recalculation must yield identical values
        assert snapshot_dict["pair"] == original_pair_value
        assert snapshot_dict["outer"] == original_outer_value