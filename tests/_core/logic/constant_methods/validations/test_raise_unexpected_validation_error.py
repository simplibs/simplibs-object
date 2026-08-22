import pytest
from typing import Any
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.constant_methods.validations.raise_unexpected_validation_error import (
    raise_unexpected_validation_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, value, original_exception",
    [
        ("ValidatorClass", 42, KeyError("missing_key")),
        ("UserObject", "bad_data", ZeroDivisionError("division by zero")),
    ],
)
def test_raise_unexpected_validation_error(
    subtests, class_name: str, value: Any, original_exception: Exception
) -> None:
    """Test that intercepting an unexpected error in _validate raises SimpleRuntimeError wrapping original exception."""

    dummy_cls = Mock()
    dummy_cls.__name__ = class_name

    assert_exception_function(
        subtests,
        raise_unexpected_validation_error,

        invalid_params=(dummy_cls, value, original_exception),
        exception_type=SimpleRuntimeError,

        error_name="VALIDATION ERROR",
        label="value",
        value=value,
        expected="A value that satisfies the user-defined validation logic.",
        problem=(
            f"The value could not be validated successfully.",
            f"An unexpected exception occurred during validation in '{class_name}'. ",
        ),
        context=(
            f"The validation pipeline for '{class_name}' intercepted an exception "
            f"raised inside the user-defined '_validate' method. ",
            f"This may indicate either an invalid value or an internal error in the validation logic.",
        ),
        how_to_fix=(
            "Review the intercepted exception shown at the end of this error message "
            "to determine whether the issue is caused by invalid input or a bug in "
            "the '_validate' method.",
            "If you intend to raise custom validation errors, ensure they inherit "
            "from 'SimpleObjectError' so they are handled as expected.",
            "If the error is unintended, verify that the validation logic does not "
            "perform unsafe operations or rely on assumptions that may not hold.",
        ),
        exception=original_exception,

        verbose=False,
    )