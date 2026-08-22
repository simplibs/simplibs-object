from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._helpers._validations.raise_calculate_default_failed import (
    raise_calculate_default_failed,
)


def test_raise_calculate_default_failed(subtests) -> None:
    """Tests that raise_calculate_default_failed raises SimpleRuntimeError."""

    def mock_logic(cls, a, b):
        return a / b

    params = (10, 0)
    original_exception = ZeroDivisionError("division by zero")

    assert_exception_function(
        subtests,
        raise_calculate_default_failed,
        invalid_params=(mock_logic, params, original_exception),
        exception_type=SimpleRuntimeError,
        error_name="CALCULATE DEFAULT FAILED ERROR",
        label="calculate_default_failed",
        value={
            "logic": "mock_logic",
            "params": params,
        },
        expected="A valid logic callable that executes successfully with default inner values",
        problem=(
            "Failed to infer default value using logic function 'mock_logic'. ",
            "Execution raised ZeroDivisionError: division by zero",
        ),
        context=(
            "Attempted to execute logic 'mock_logic' with inferred inner default arguments, ",
            "to automatically determine the value type of a dynamic composite object.",
        ),
        how_to_fix=(
            "Ensure the provided 'logic' callable handles initial default child values without raising exceptions.",
            "Verify that default values of all 'inners' are compatible with the operations inside 'logic'.",
            "Alternatively, explicitly specify the 'value_type' parameter in create_object_class / create_simple_object.",
        ),
        exception=original_exception,
        verbose=False,
    )