import pytest
from typing import Any
from unittest.mock import Mock
from simplibs.exception.testing import (
    assert_function_valid_input,
    assert_exception_function,
)
from simplibs.object.tools.randomize._validations.validate_instance_is_simple_constant_base import (
    validate_instance_is_simple_constant_base,
)
from simplibs.object.SimpleConstant import SimpleConstant
from simplibs.object.exceptions import SimpleRuntimeError


class DummyConstant(SimpleConstant):
    """Dummy subclass to simulate a valid SimpleConstant instance."""
    _type = int
    _default = 1


def test_valid_instance(subtests) -> None:
    """Test happy path for valid SimpleConstant instances."""
    dummy_instance = Mock(spec=SimpleConstant)

    assert_function_valid_input(
        subtests,
        validate_instance_is_simple_constant_base,
        valid_params=(dummy_instance,),
        verbose=False,
    )


@pytest.mark.parametrize(
    "invalid_instance",
    [
        "not_a_constant",
        123,
        None,
        [1, 2, 3],
        object(),
    ],
)
def test_invalid_instance(subtests, invalid_instance: Any) -> None:
    """Test that non-SimpleConstant instances raise SimpleRuntimeError."""
    received_type = type(invalid_instance).__name__

    assert_exception_function(
        subtests,
        validate_instance_is_simple_constant_base,
        invalid_params=(invalid_instance,),
        exception_type=SimpleRuntimeError,
        error_name="INVALID INSTANCE TYPE ERROR",
        label="instance",
        expected="An instance inheriting from SimpleConstant or SimpleObject.",
        value=received_type,
        problem=(
            "Provided instance does not derive from SimpleConstant.",
            "Random data fill operations require a Simple framework instance.",
        ),
        context=(
            f"Received object: {invalid_instance!r}",
            f"Received type: '{received_type}'",
        ),
        how_to_fix=(
            "Pass a valid SimpleConstant or SimpleObject instance to random_data_filler / randomize_value.",
            "Ensure the object was initialized via the Simple ecosystem base classes.",
        ),
        exception=TypeError,
        verbose=False,
    )