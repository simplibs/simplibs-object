import pytest
from typing import Any
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.constant_methods.validations.raise_validation_error import (
    raise_validation_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


def dummy_validate_func(val):
    """Dummy validation function for code extraction tests."""
    # Check value condition
    return val > 0


@pytest.mark.parametrize(
    "class_name, invalid_value",
    [
        ("PositiveIntClass", -5),
        ("EmailValidator", "invalid_email"),
    ],
)
def test_raise_validation_error(
    subtests, class_name: str, invalid_value: Any
) -> None:
    """Test that boolean validation failure raises SimpleRuntimeError containing extracted code lines."""

    dummy_cls = Mock()
    dummy_cls.__name__ = class_name
    dummy_cls.meta.validate = dummy_validate_func

    expected_extracted_lines = [
        "    return val > 0"
    ]

    assert_exception_function(
        subtests,
        raise_validation_error,

        invalid_params=(dummy_cls, invalid_value),
        exception_type=SimpleRuntimeError,

        error_name="VALIDATION ERROR",
        label="value",
        value=invalid_value,
        expected="A value that satisfies the user-defined validation logic.",
        problem="The provided value did not pass the user-defined validation rules.",
        context=(
            f"The '_validate' method of '{class_name}' returned False, indicating "
            f"that the value does not meet the required validation criteria."
        ),
        how_to_fix=(
            "Review the validation logic shown below to understand why the value "
            "was rejected:",
            *expected_extracted_lines,
            "Ensure that the input value matches the assumptions and constraints "
            "defined in your validation method.",
            "If you intend to raise custom validation errors instead of returning "
            "False, use 'SimpleObjectError' or 'cls.bool_or_raise_validate_error()'.",
        ),
        exception=ValueError,

        verbose=False,
    )


def test_raise_validation_error_fallback(subtests) -> None:
    """Test fallback placeholder behavior when source extraction fails."""

    dummy_cls = Mock()
    dummy_cls.__name__ = "FallbackClass"
    # Cause source extraction to fail (e.g. invalid attribute object)
    dummy_cls.meta.validate = None

    assert_exception_function(
        subtests,
        raise_validation_error,

        invalid_params=(dummy_cls, "some_value"),
        exception_type=SimpleRuntimeError,

        error_name="VALIDATION ERROR",
        label="value",
        value="some_value",
        expected="A value that satisfies the user-defined validation logic.",
        problem="The provided value did not pass the user-defined validation rules.",
        context=(
            "The '_validate' method of 'FallbackClass' returned False, indicating "
            "that the value does not meet the required validation criteria."
        ),
        how_to_fix=(
            "Review the validation logic shown below to understand why the value "
            "was rejected:",
            "    <source code not available>",
            "Ensure that the input value matches the assumptions and constraints "
            "defined in your validation method.",
            "If you intend to raise custom validation errors instead of returning "
            "False, use 'SimpleObjectError' or 'cls.bool_or_raise_validate_error()'.",
        ),
        exception=ValueError,

        verbose=False,
    )