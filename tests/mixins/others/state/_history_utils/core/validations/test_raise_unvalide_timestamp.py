from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.core.validations.raise_unvalide_timestamp import (
    raise_unvalide_timestamp,
)


def test_raise_unvalide_timestamp(subtests) -> None:
    """Tests that raise_unvalide_timestamp raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyHistoryClass"
    invalid_ts = 123456789

    assert_exception_function(
        subtests,
        raise_unvalide_timestamp,
        invalid_params=(dummy_instance, invalid_ts),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY TIMESTAMP ERROR",
        label="timestamp",
        expected="A valid datetime object.",
        value="int",
        problem=(
            "Invalid timestamp reference provided.",
            "History lookup requires a datetime value.",
        ),
        context=(
            "History lookup attempted on instance 'MyHistoryClass'.",
            "Provided value type: int",
        ),
        how_to_fix=(
            "Ensure the reference is a datetime object.",
            "Use `go_to_timestamp` or `find_snapshot` with a valid datetime.",
            "Do not pass integers, strings, or other types.",
        ),
        exception=TypeError,
        verbose=False,
    )