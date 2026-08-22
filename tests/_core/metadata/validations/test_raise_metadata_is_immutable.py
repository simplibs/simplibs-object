from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.validations.raise_metadata_is_immutable import (
    raise_metadata_is_immutable,
)


def test_raise_metadata_is_immutable(subtests, sample_object_classes) -> None:
    """Tests that raise_metadata_is_immutable raises SimpleDefinitionError."""

    _, MyTestObject = sample_object_classes

    attr_name = "value_type"
    current_value = dict
    new_value = list

    assert_exception_function(
        subtests,
        raise_metadata_is_immutable,
        invalid_params=(attr_name, current_value, new_value, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="METADATA IMMUTABILITY ERROR",
        label="metadata field",
        value=new_value,
        expected="Metadata fields are write-once.",
        problem=(
            f"The field '{attr_name}' is already initialized.",
            f"Current value: {repr(current_value)}",
        ),
        context="Attempted overwrite inside metadata of class 'MyTestObject'.",
        how_to_fix=(
            "Do not overwrite initialized metadata fields.",
            "Only fields holding UNSET may be assigned.",
            "If you need dynamic state, use a dedicated cache slot.",
        ),
        exception=AttributeError,
        verbose=False,
    )