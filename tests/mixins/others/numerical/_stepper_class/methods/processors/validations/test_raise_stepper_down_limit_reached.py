from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.numerical._stepper_class.methods.processors.validations.raise_stepper_down_limit_reached import (
    raise_stepper_down_limit_reached,
)


def test_raise_stepper_down_limit_reached(subtests) -> None:
    """Tests that raise_stepper_down_limit_reached raises SimpleRuntimeError."""

    dummy_stepper = Mock()
    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyStepperObj"
    dummy_instance.value = 10
    dummy_stepper._instance = dummy_instance
    dummy_stepper.down_limit = 5

    new_invalid_value = 2

    assert_exception_function(
        subtests,
        raise_stepper_down_limit_reached,
        invalid_params=(dummy_stepper, new_invalid_value),
        exception_type=SimpleRuntimeError,
        error_name="STEPPER DOWN LIMIT ERROR",
        label="new value",
        value=new_invalid_value,
        expected="Value >= 5",
        problem=(
            "The step operation attempted to decrease the value below the "
            "configured down limit."
        ),
        context=(
            "Instance type: MyStepperObj.",
            "Current value: 10.",
            "Down limit: 5.",
            "The stepper enforces numeric boundaries to prevent invalid state transitions.",
        ),
        how_to_fix=(
            "Increase the down limit if lower values should be allowed.",
            "Adjust the step value to avoid crossing the limit.",
            "Disable limit enforcement if this behavior is intentional.",
        ),
        exception=ValueError,
        verbose=False,
    )