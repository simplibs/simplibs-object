from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.numerical._stepper_class.processors.validations.raise_stepper_invalid_instance import (
    raise_stepper_invalid_instance,
)


def test_raise_stepper_invalid_instance(subtests) -> None:
    """Tests that raise_stepper_invalid_instance raises SimpleRuntimeError."""

    invalid_instance = "plain_string_instance"
    expected_type = Mock()
    expected_type.__name__ = "SimpleInstanceType"

    assert_exception_function(
        subtests,
        raise_stepper_invalid_instance,
        invalid_params=(invalid_instance, expected_type),
        exception_type=SimpleRuntimeError,
        error_name="STEPPER INSTANCE ERROR",
        label="instance",
        value=invalid_instance,
        expected="Instance implementing SimpleInstanceType",
        problem=(
            "The provided object does not satisfy the required Simple instance "
            "protocol. The Stepper can only operate on valid Simple instances "
            "that expose a numeric `value` attribute and support mixin operations."
        ),
        context=(
            "Received type: str.",
            "Stepper requires a Simple instance with a numeric value.",
            "Invalid instances cannot participate in numeric stepping operations.",
        ),
        how_to_fix=(
            "Ensure that the object passed to Stepper is a valid Simple instance.",
            "Verify that the instance implements the required protocol.",
            "Check that the instance exposes a numeric `value` attribute.",
        ),
        exception=TypeError,
        verbose=False,
    )