import pytest
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.object_methods.validations.raise_too_many_positional_args_error import (
    raise_too_many_positional_args_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, given_count, allowed_count",
    [
        ("MyComposite", 4, 2),
        ("PointObject", 3, 2),
    ],
)
def test_raise_too_many_positional_args_error(
    subtests, class_name: str, given_count: int, allowed_count: int
) -> None:
    """Test that passing more positional args than inner elements raises SimpleRuntimeError."""

    dummy_cls = Mock()
    dummy_cls.__name__ = class_name

    assert_exception_function(
        subtests,
        raise_too_many_positional_args_error,

        invalid_params=(dummy_cls, given_count, allowed_count),
        exception_type=SimpleRuntimeError,

        error_name="INVALID PARAMETERS",
        label="args",
        value=f"{given_count} positional arguments",
        expected=f"At most {allowed_count} positional arguments matching inner elements",
        problem=(
            f"The class '{class_name}' received more positional arguments than "
            f"the number of defined inner elements."
        ),
        context=(
            f"During parameter processing for '{class_name}.calculate_value', the "
            f"system detected an argument count mismatch."
        ),
        how_to_fix=(
            f"Provide no more than {allowed_count} positional arguments.",
            "If you intended to use named parameters, pass them as keyword arguments.",
            "Ensure that each positional argument corresponds to an inner element "
            "in the order defined by the class.",
        ),
        exception=ValueError,

        verbose=False,
    )