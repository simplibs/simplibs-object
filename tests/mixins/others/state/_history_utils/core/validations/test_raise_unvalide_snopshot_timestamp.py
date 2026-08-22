from datetime import datetime
from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.core.validations.raise_unvalide_snopshot_timestamp import (
    raise_unvalide_snopshot_timestamp,
)


def test_raise_unvalide_snopshot_timestamp(subtests) -> None:
    """Tests that raise_unvalide_snopshot_timestamp raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyHistoryClass"

    ts_1 = datetime(2026, 1, 1, 12, 0, 0)
    ts_2 = datetime(2026, 1, 2, 12, 0, 0)
    dummy_instance._history = ((ts_1, "state1"), (ts_2, "state2"))

    missing_ts = datetime(2026, 8, 18, 10, 0, 0)

    assert_exception_function(
        subtests,
        raise_unvalide_snopshot_timestamp,
        invalid_params=(dummy_instance, missing_ts),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY SNAPSHOT TIMESTAMP ERROR",
        label="snapshot timestamp",
        expected="A timestamp that exists in recorded history.",
        value=missing_ts,
        problem=(
            "Snapshot with the provided timestamp was not found.",
            f"Timestamp {missing_ts!r} does not match any recorded snapshot.",
        ),
        context=(
            "History lookup attempted on instance 'MyHistoryClass'.",
            f"Available timestamps: {(ts_1, ts_2)}",
        ),
        how_to_fix=(
            "Ensure the timestamp refers to an existing snapshot.",
            "Use `history` or `export_history_to_dict` to inspect available timestamps.",
            "Snapshot timestamps are stored exactly as datetime values.",
        ),
        exception=KeyError,
        verbose=False,
    )