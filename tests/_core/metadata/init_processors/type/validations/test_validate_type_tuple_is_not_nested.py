from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.validate_type_tuple_is_not_nested import (
    validate_type_tuple_is_not_nested,
)


def test_validate_type_tuple_is_not_nested_pass(sample_object_classes) -> None:
    """Tests that a non-nested type inside a tuple passes validation."""

    MyTestConstant, MyTestObject = sample_object_classes

    validate_type_tuple_is_not_nested(int, (int, str), MyTestObject)


def test_validate_type_tuple_is_not_nested_raises_error(subtests, sample_object_classes) -> None:
    """Tests that a nested tuple inside _type raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    nested_element = (str, float)
    type_tuple = (int, nested_element)

    assert_exception_function(
        subtests,
        validate_type_tuple_is_not_nested,
        invalid_params=(nested_element, type_tuple, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        value=type_tuple,
        expected="A flat tuple of types.",
        problem="The '_type' tuple contains a nested tuple.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Flatten the tuple into a single sequence.",
            "Nested tuples cannot be processed.",
            "Example: (int, (str, float)) → (int, str, float).",
            "Acceptable definitions:",
            "class MyTestObject(SimpleObject):",
            "    _type = int",
            "    _type = int | str",
            "    _type = (int, str)",
            "    ...",
        ),
        exception=TypeError,
        verbose=False,
    )