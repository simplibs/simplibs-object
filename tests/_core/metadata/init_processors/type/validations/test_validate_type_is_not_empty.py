from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.validate_type_is_not_empty import (
    validate_type_is_not_empty,
)


def test_validate_type_is_not_empty_pass(sample_object_classes) -> None:
    """Tests that a non-empty _type attribute passes validation."""

    MyTestConstant, MyTestObject = sample_object_classes

    validate_type_is_not_empty(int, MyTestObject)
    validate_type_is_not_empty((int, str), MyTestObject)


def test_validate_type_is_not_empty_raises_error(subtests, sample_object_classes) -> None:
    """Tests that an empty container for _type raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    empty_tuple = ()

    assert_exception_function(
        subtests,
        validate_type_is_not_empty,
        invalid_params=(empty_tuple, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        value=empty_tuple,
        expected="A non-empty type, UnionType, or tuple of types.",
        problem="The '_type' attribute evaluates to an empty value.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Define '_type' as a real type or a non-empty collection of types.",
            "Empty definitions cannot be validated or mapped.",
            "Update '_type' to reflect the actual allowed value structure.",
            "Acceptable definitions:",
            "class MyTestObject(SimpleObject):",
            "    _type = int",
            "    _type = int | str",
            "    _type = (int, str)",
            "    ...",
        ),
        exception=ValueError,
        verbose=False,
    )