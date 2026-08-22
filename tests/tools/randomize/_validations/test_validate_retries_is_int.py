import pytest
from typing import Any
from simplibs.exception.testing import (
    assert_function_valid_input,
    assert_exception_function,
)
from simplibs.object.tools.randomize._validations.validate_retries_is_int import (
    validate_retries_is_int,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "valid_retries",
    [
        0,
        1,
        10,
        -5,
    ],
)
def test_valid_retries_int(subtests, valid_retries: int) -> None:
    """Test happy path for integer inputs."""
    assert_function_valid_input(
        subtests,
        validate_retries_is_int,
        valid_params=(valid_retries,),
        verbose=False,
    )


@pytest.mark.parametrize(
    "invalid_retries",
    [
        True,
        False,
        "5",
        5.0,
        None,
        [5],
    ],
)
def test_invalid_retries_type(subtests, invalid_retries: Any) -> None:
    """Test that non-int types and booleans raise SimpleRuntimeError."""
    received_type = type(invalid_retries).__name__

    assert_exception_function(
        subtests,
        validate_retries_is_int,
        invalid_params=(invalid_retries,),
        exception_type=SimpleRuntimeError,
        error_name="INVALID RETRIES TYPE ERROR",
        label="retries",
        expected="An integer instance representing attempt count.",
        value=received_type,
        problem=(
            "Retries parameter must be an integer.",
            f"Received type '{received_type}' instead of 'int'.",
        ),
        context=(
            f"Received argument: {invalid_retries!r}",
        ),
        how_to_fix=(
            "Pass an integer value for retries, e.g. retries=5.",
            "Do not pass floats, strings, or boolean flags as retries.",
        ),
        exception=TypeError,
        verbose=False,
    )