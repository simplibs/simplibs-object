from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.core_mixins._utils.serialization.validations.raise_missing_value_key import (
    raise_missing_value_key,
)


def test_raise_missing_value_key(subtests) -> None:
    """Tests that raise_missing_value_key raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MySerializableClass"

    missing_key = "value"
    full_path = ("root", "leaf_node", "value")

    assert_exception_function(
        subtests,
        raise_missing_value_key,
        invalid_params=(dummy_instance, missing_key, full_path),
        exception_type=SimpleRuntimeError,
        error_name="STATE DICT MISSING VALUE KEY",
        label="value key",
        value="value",
        expected="Key 'value' to exist in the dictionary.",
        problem=(
            "A required value key is missing in the state dictionary.",
            "The key 'value' was expected but not found.",
        ),
        context=(
            "State import attempted on instance 'MySerializableClass'.",
            "Traversal path: ('root', 'leaf_node', 'value')",
            "Atomic VALUE nodes must contain their final key.",
        ),
        how_to_fix=(
            "Ensure the state dictionary contains all required VALUE keys.",
            "Use `to_dict()` to generate a correct structure.",
            "Verify that no VALUE field is missing or removed.",
        ),
        exception=KeyError,
        verbose=False,
    )