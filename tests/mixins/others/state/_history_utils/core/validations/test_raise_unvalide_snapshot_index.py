from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.core.validations.raise_unvalide_snapshot_index import (
    raise_unvalide_snapshot_index,
)


def test_raise_unvalide_snapshot_index(subtests) -> None:
    """Tests that raise_unvalide_snapshot_index raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyHistoryClass"
    dummy_instance._history_count = 3
    invalid_index = 5

    assert_exception_function(
        subtests,
        raise_unvalide_snapshot_index,
        invalid_params=(dummy_instance, invalid_index),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY SNAPSHOT INDEX ERROR",
        label="snapshot index",
        expected="Integer in range 0 <= index < 3",
        value=invalid_index,
        problem=(
            "Invalid snapshot index provided.",
            "Index 5 is outside the valid range of recorded history.",
        ),
        context=(
            "History lookup attempted on instance 'MyHistoryClass'.",
            "Total number of snapshots: 3",
        ),
        how_to_fix=(
            "Ensure the index refers to an existing snapshot.",
            "Use `history_index` or inspect `history` to determine valid indices.",
            "Snapshot indices start at 0 and increase sequentially.",
        ),
        exception=IndexError,
        verbose=False,
    )