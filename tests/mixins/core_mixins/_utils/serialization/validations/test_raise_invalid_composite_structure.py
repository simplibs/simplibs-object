from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.core_mixins._utils.serialization.validations.raise_invalid_composite_structure import (
    raise_invalid_composite_structure,
)


def test_raise_invalid_composite_structure(subtests) -> None:
    """Tests that raise_invalid_composite_structure raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MySerializableClass"

    key = "sub_component"
    invalid_value = "string_instead_of_dict"
    full_path = ("root", "sub_component")

    assert_exception_function(
        subtests,
        raise_invalid_composite_structure,
        invalid_params=(dummy_instance, key, invalid_value, full_path),
        exception_type=SimpleRuntimeError,
        error_name="STATE DICT INVALID COMPOSITE STRUCTURE",
        label="composite structure",
        value="'string_instead_of_dict'",
        expected="A dictionary at key 'sub_component'.",
        problem=(
            "Invalid structure encountered in composite branch.",
            "Expected a dictionary at key 'sub_component', but got str.",
        ),
        context=(
            "State import attempted on instance 'MySerializableClass'.",
            "Traversal path: ('root', 'sub_component')",
            "Composite nodes must be represented as nested dictionaries.",
        ),
        how_to_fix=(
            "Ensure that all composite branches in the state dictionary are dictionaries.",
            "Use `to_dict()` to generate a correct nested structure.",
            "Verify that no composite node was replaced by a scalar or list.",
        ),
        exception=KeyError,
        verbose=False,
    )