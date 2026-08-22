from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.core_mixins._utils.serialization.validations.raise_unvalid_state_dict_input import (
    raise_unvalid_state_dict_input,
)


def test_raise_unvalid_state_dict_input(subtests) -> None:
    """Tests that raise_unvalid_state_dict_input raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MySerializableClass"

    invalid_input = ["not", "a", "dict"]

    assert_exception_function(
        subtests,
        raise_unvalid_state_dict_input,
        invalid_params=(dummy_instance, invalid_input),
        exception_type=SimpleRuntimeError,
        error_name="STATE DICT INPUT ERROR",
        label="state dictionary",
        value="['not', 'a', 'dict']",
        expected="A dictionary mapping node paths to values.",
        problem=(
            "Invalid input provided for state reconstruction.",
            "State import requires a dictionary structure.",
        ),
        context=(
            "State import attempted on instance 'MySerializableClass'.",
            "Provided value type: list",
        ),
        how_to_fix=(
            "Ensure the input is a dictionary.",
            "Use `to_dict()` or `export_history_to_dict()` to generate valid structures.",
            "Do not pass lists, tuples, strings, or other unsupported types.",
        ),
        exception=TypeError,
        verbose=False,
    )