"""
Tests for `create_new_instance(instance, snapshot)`.
"""
from simplibs.object.mixins._common_logic.immutability.with_constant.utils import (
    create_new_instance,
)


class TestCreateNewInstance:

    def test_returns_new_instance_of_same_class(self, immutable_outer_instance):
        snapshot = immutable_outer_instance._build_snapshot()
        result = create_new_instance(immutable_outer_instance, snapshot)
        assert type(result) is type(immutable_outer_instance)
        assert result is not immutable_outer_instance

    def test_restores_snapshot_values(self, immutable_outer_instance):
        snapshot = immutable_outer_instance._build_snapshot()
        result = create_new_instance(immutable_outer_instance, snapshot)
        assert result._build_snapshot() == snapshot

    def test_modified_snapshot_is_applied(self, immutable_outer_instance):
        original_snapshot = immutable_outer_instance._build_snapshot()
        # Create a modified snapshot of equal length with altered values
        modified_snapshot = tuple(
            value + 100 if isinstance(value, int) else value
            for value in original_snapshot
        )
        result = create_new_instance(immutable_outer_instance, modified_snapshot)
        assert result._build_snapshot() == modified_snapshot
        assert result._build_snapshot() != original_snapshot