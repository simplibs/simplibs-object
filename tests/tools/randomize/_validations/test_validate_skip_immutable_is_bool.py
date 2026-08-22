import pytest
from typing import Any
from simplibs.exception.testing import (
    assert_function_valid_input,
    assert_exception_function,
)
from simplibs.object.tools.randomize._validations.validate_skip_immutable_is_bool import (
    validate_skip_immutable_is_bool,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "valid_flag",
    [
        True,
        False,
    ],
)
def test_valid_skip_immutable(subtests, valid_flag: bool) -> None:
    """Test happy path for boolean inputs."""
    assert_function_valid_input(
        subtests,
        validate_skip_immutable_is_bool,
        valid_params=(valid_flag,),
        verbose=False,
    )


@pytest.mark.parametrize(
    "invalid_flag",
    [
        1,
        0,
        "True",
        None,
        [True],
    ],
)
def test_invalid_skip_immutable_type(subtests, invalid_flag: Any) -> None:
    """Test that non-boolean values raise SimpleRuntimeError."""
    received_type = type(invalid_flag).__name__

    assert_exception_function(
        subtests,
        validate_skip_immutable_is_bool,
        invalid_params=(invalid_flag,),
        exception_type=SimpleRuntimeError,
        error_name="INVALID SKIP_IMMUTABLE TYPE ERROR",
        label="skip_immutable",
        expected="A boolean value (True or False).",
        value=received_type,
        problem=(
            "skip_immutable parameter must be a boolean flag.",
            f"Received type '{received_type}' instead of 'bool'.",
        ),
        context=(
            f"Received argument: {invalid_flag!r}",
        ),
        how_to_fix=(
            "Pass True or False for skip_immutable.",
        ),
        exception=TypeError,
        verbose=False,
    )