import pytest
from typing import Any
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.constant_methods.validations.raise_type_error import (
    raise_type_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, expected_types, invalid_value",
    [
        ("AgeConstant", "int", "not_an_int"),
        ("NameConstant", "str", 12345),
        ("ListConstant", "list[str]", None),
    ],
)
def test_raise_type_error(
    subtests, class_name: str, expected_types: str, invalid_value: Any
) -> None:
    """Test that type mismatch raises SimpleRuntimeError with type details."""

    dummy_cls = Mock()
    dummy_cls.__name__ = class_name
    dummy_cls.meta.value_type_name = expected_types

    assert_exception_function(
        subtests,
        raise_type_error,

        invalid_params=(dummy_cls, invalid_value),
        exception_type=SimpleRuntimeError,

        error_name="TYPE ERROR",
        label="value",
        value=invalid_value,
        expected=f"Instance of type '{expected_types}'",
        problem=(
            f"The provided value does not match the required type for constant "
            f"'{class_name}'."
        ),
        context=(
            f"Runtime type enforcement for '{class_name}' requires a value of "
            f"type {expected_types}."
        ),
        how_to_fix=(
            f"Ensure that the provided value is an instance of: {expected_types}.",
            "Check whether any unintended type conversion or transformation "
            "occurs before this validation.",
        ),
        exception=TypeError,

        verbose=False,
    )