from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.core_mixins._utils.serialization.validations.raise_missing_composite_key import (
    raise_missing_composite_key,
)


def test_raise_missing_composite_key(subtests) -> None:
    """Tests that raise_missing_composite_key raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MySerializableClass"

    missing_key = "nested_node"
    full_path = ("root", "nested_node")

    assert_exception_function(
        subtests,
        raise_missing_composite_key,
        invalid_params=(dummy_instance, missing_key, full_path),
        exception_type=SimpleRuntimeError,
        error_name="STATE DICT MISSING KEY",
        label="composite key",
        value="nested_node",
        expected="Key 'nested_node' to exist in nested dictionary structure.",
        problem=(
            "A required key is missing in the composite branch of the state dictionary.",
            "The key 'nested_node' was expected but not found.",
        ),
        context=(
            "State import attempted on instance 'MySerializableClass'.",
            "Traversal path: ('root', 'nested_node')",
            "Composite nodes must contain all required nested keys.",
        ),
        how_to_fix=(
            "Ensure the state dictionary contains all composite keys according to the object's structure.",
            "Use `to_dict()` to generate a correct structure.",
            "Verify that nested dictionaries are complete and not partially missing.",
        ),
        exception=KeyError,
        verbose=False,
    )