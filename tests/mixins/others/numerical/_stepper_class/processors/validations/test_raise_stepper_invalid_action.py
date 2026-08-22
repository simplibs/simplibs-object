from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.numerical._stepper_class.processors.validations.raise_stepper_invalid_action import (
    raise_stepper_invalid_action,
)


def test_raise_stepper_invalid_action(subtests) -> None:
    """Tests that raise_stepper_invalid_action raises SimpleRuntimeError."""

    dummy_stepper = Mock()
    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyStepperObj"
    dummy_instance.value = 10
    dummy_stepper._instance = dummy_instance

    invalid_action = "not_a_callable"

    assert_exception_function(
        subtests,
        raise_stepper_invalid_action,
        invalid_params=(dummy_stepper, invalid_action),
        exception_type=SimpleRuntimeError,
        error_name="STEPPER LIMIT ACTION ERROR",
        label="limit action",
        value=invalid_action,
        expected="A callable object (function, method, or callable instance).",
        problem=(
            "The provided limit action is not callable. "
            "Stepper limit actions must be executable callbacks."
        ),
        context=(
            "Instance type: MyStepperObj.",
            "Current value: 10.",
            "Limit actions are executed when the stepper reaches configured boundaries.",
            "Non-callable objects cannot be invoked as callbacks.",
        ),
        how_to_fix=(
            "Provide a callable object, such as a function or method.",
            "Ensure that the action does not require arguments when invoked.",
            "If you need a more complex action, wrap it into a callable object.",
        ),
        exception=TypeError,
        verbose=False,
    )