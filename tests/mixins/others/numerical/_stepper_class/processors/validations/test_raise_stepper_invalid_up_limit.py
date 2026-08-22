from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.numerical._stepper_class.processors.validations.raise_stepper_invalid_up_limit import (
    raise_stepper_invalid_up_limit,
)


def test_raise_stepper_invalid_up_limit(subtests) -> None:
    """Tests that raise_stepper_invalid_up_limit raises SimpleRuntimeError."""

    dummy_stepper = Mock()
    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyStepperObj"
    dummy_instance.value = 50
    dummy_stepper._instance = dummy_instance
    dummy_stepper.down_limit = 100

    invalid_up_limit = 80

    assert_exception_function(
        subtests,
        raise_stepper_invalid_up_limit,
        invalid_params=(dummy_stepper, invalid_up_limit),
        exception_type=SimpleRuntimeError,
        error_name="STEPPER LIMIT CONFIGURATION ERROR",
        label="up limit",
        value=invalid_up_limit,
        expected="Value >= 100",
        problem=(
            "The provided upper limit is lower than the configured down limit. "
            "This creates an invalid numeric boundary configuration."
        ),
        context=(
            "Instance type: MyStepperObj.",
            "Current value: 50.",
            "Down limit: 100.",
            "Attempted up limit: 80.",
            "The stepper requires consistent numeric boundaries where down_limit <= up_limit.",
        ),
        how_to_fix=(
            "Set the upper limit to a value greater than or equal to the down limit.",
            "If you need to restrict the allowed range, lower the down limit first.",
            "Ensure that both limits reflect a valid numeric interval.",
        ),
        exception=ValueError,
        verbose=False,
    )