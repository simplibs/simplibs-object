from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.numerical._stepper_class.processors.validations.raise_stepper_invalid_down_limit import (
    raise_stepper_invalid_down_limit,
)


def test_raise_stepper_invalid_down_limit(subtests) -> None:
    """Tests that raise_stepper_invalid_down_limit raises SimpleRuntimeError."""

    dummy_stepper = Mock()
    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyStepperObj"
    dummy_instance.value = 50
    dummy_stepper._instance = dummy_instance
    dummy_stepper.up_limit = 20

    invalid_down_limit = 30

    assert_exception_function(
        subtests,
        raise_stepper_invalid_down_limit,
        invalid_params=(dummy_stepper, invalid_down_limit),
        exception_type=SimpleRuntimeError,
        error_name="STEPPER LIMIT CONFIGURATION ERROR",
        label="down limit",
        value=invalid_down_limit,
        expected="Value <= 20",
        problem=(
            "The provided down limit is higher than the configured up limit. "
            "This creates an invalid numeric boundary configuration."
        ),
        context=(
            "Instance type: MyStepperObj.",
            "Current value: 50.",
            "Up limit: 20.",
            "Attempted down limit: 30.",
            "The stepper requires consistent numeric boundaries where down_limit <= up_limit.",
        ),
        how_to_fix=(
            "Set the down limit to a value lower than or equal to the up limit.",
            "If you need to expand the allowed range, increase the up limit first.",
            "Ensure that both limits reflect a valid numeric interval.",
        ),
        exception=ValueError,
        verbose=False,
    )