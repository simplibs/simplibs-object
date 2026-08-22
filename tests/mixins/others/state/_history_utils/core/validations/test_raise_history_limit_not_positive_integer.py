from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.core.validations.raise_history_limit_not_positive_integer import (
    raise_history_limit_not_positive_integer,
)


def test_raise_history_limit_not_positive_integer(subtests) -> None:
    """Tests that raise_history_limit_not_positive_integer raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyHistoryClass"
    invalid_limit = -5

    assert_exception_function(
        subtests,
        raise_history_limit_not_positive_integer,
        invalid_params=(dummy_instance, invalid_limit),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY LIMIT ERROR",
        label="history limit",
        expected="A positive integer (value >= 1).",
        value=invalid_limit,
        problem=(
            "Invalid history limit provided.",
            "History limit must be a positive integer greater than or equal to 1.",
        ),
        context=(
            "History limit assignment attempted on instance 'MyHistoryClass'.",
            "Provided value type: int",
        ),
        how_to_fix=(
            "Ensure the limit is an integer.",
            "Ensure the limit is at least 1.",
            "Example valid values: 1, 5, 10, 100.",
        ),
        exception=ValueError,
        verbose=False,
    )