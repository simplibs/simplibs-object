from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.state._history_utils.transfer.validations.raise_unvalide_history_import_file import (
    raise_unvalide_history_import_file,
)


def test_raise_unvalide_history_import_file(subtests) -> None:
    """Tests that raise_unvalide_history_import_file raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyClass"

    invalid_value = ["not", "a", "dict"]

    assert_exception_function(
        subtests,
        raise_unvalide_history_import_file,
        invalid_params=(dummy_instance, invalid_value),
        exception_type=SimpleRuntimeError,
        error_name="HISTORY IMPORT FORMAT ERROR",
        label="history import container",
        expected="A dictionary containing OWNER_CLASS and HISTORY fields.",
        value="list",
        problem=(
            "Invalid history import format.",
            "History import requires a dictionary structure."
        ),
        context=(
            "History import attempted on instance 'MyClass'.",
            "Provided value type: list"
        ),
        how_to_fix=(
            "Ensure the input is a dictionary.",
            "Use `export_history_to_dict()` to generate a valid import structure.",
            "Do not pass lists, tuples, strings, or other unsupported types."
        ),
        exception=TypeError,
        verbose=False,
    )