"""
Tests for `reacalculate_inners(snapshot_dict, meta, new_value)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_composite.utils import (
    reacalculate_inners,
)


class TestReacalculateInners:

    def test_writes_decomposed_values_into_snapshot_dict(self, immutable_outer_instance):
        pair_instance = immutable_outer_instance._nodes_dict["pair"][0]
        snapshot_dict = {}

        reacalculate_inners(snapshot_dict, pair_instance.meta, 42)

        # Pair._decompose(42) -> (42, 0) based on fixture definition
        assert snapshot_dict["first"] == 42
        assert snapshot_dict["second"] == 0

    def test_recurses_into_nested_composite_inners(self, immutable_outer_instance):
        snapshot_dict = {}
        reacalculate_inners(snapshot_dict, immutable_outer_instance.meta, 99)

        assert snapshot_dict["pair"] == 99
        assert snapshot_dict["third"] == 0
        # Descent into pair: Pair._decompose(99) -> (99, 0)
        assert snapshot_dict["first"] == 99
        assert snapshot_dict["second"] == 0