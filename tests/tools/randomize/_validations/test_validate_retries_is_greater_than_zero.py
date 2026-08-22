import pytest
from simplibs.exception.testing import (
    assert_function_valid_input,
    assert_exception_function,
)
from simplibs.object.tools.randomize._validations.validate_retries_is_greater_than_zero import (
    validate_retries_is_greater_than_zero,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "valid_retries",
    [
        1,
        5,
        100,
    ],
)
def test_valid_retries_greater_than_zero(subtests, valid_retries: int) -> None:
    """Test happy path for retry counts strictly greater than zero."""
    assert_function_valid_input(
        subtests,
        validate_retries_is_greater_than_zero,
        valid_params=(valid_retries,),
        verbose=False,
    )


@pytest.mark.parametrize(
    "invalid_retries",
    [
        0,
        -1,
        -10,
    ],
)
def test_invalid_retries_bounds(subtests, invalid_retries: int) -> None:
    """Test that retry values <= 0 raise SimpleRuntimeError."""
    assert_exception_function(
        subtests,
        validate_retries_is_greater_than_zero,
        invalid_params=(invalid_retries,),
        exception_type=SimpleRuntimeError,
        error_name="INVALID RETRIES BOUNDS ERROR",
        label="retries",
        expected="An integer strictly greater than 0 (e.g. 1, 5, 10).",
        value=invalid_retries,
        problem=(
            "Retries parameter must be a positive non-zero integer.",
            f"Received value {invalid_retries}, which allows zero attempts for value generation.",
        ),
        context=(
            f"Configured retries count: {invalid_retries}",
        ),
        how_to_fix=(
            "Provide a retries value >= 1 (default recommended is 5).",
            "Do not pass zero or negative numbers as retries count.",
        ),
        exception=ValueError,
        verbose=False,
    )