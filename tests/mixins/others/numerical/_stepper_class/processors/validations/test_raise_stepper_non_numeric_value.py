from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.numerical._stepper_class.processors.validations.raise_stepper_non_numeric_value import (
    raise_stepper_non_numeric_value,
)


def test_raise_stepper_non_numeric_value(subtests) -> None:
    """Tests that raise_stepper_non_numeric_value raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyStepperObj"
    invalid_value = "non_numeric_string"

    assert_exception_function(
        subtests,
        raise_stepper_non_numeric_value,
        invalid_params=(dummy_instance, invalid_value),
        exception_type=SimpleRuntimeError,
        error_name="STEPPER VALUE TYPE ERROR",
        label="instance.value",
        value=invalid_value,
        expected="A numeric type (int, float, or any subclass of Number).",
        problem=(
            "The instance's value is not numeric. Stepper operations require "
            "a numeric value to perform increments, decrements, and limit checks."
        ),
        context=(
            "Instance type: MyStepperObj.",
            "Received value type: 'str'.",
            "Stepper can only operate on numeric values that support arithmetic operations.",
        ),
        how_to_fix=(
            "Ensure that the instance's `value` attribute is numeric.",
            "If the value comes from a composite calculation, verify that the composite returns a number.",
            "If the value is user-provided, validate or convert it before assigning it to the instance.",
        ),
        exception=TypeError,
        verbose=False,
    )