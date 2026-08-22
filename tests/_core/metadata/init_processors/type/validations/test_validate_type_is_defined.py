from simplibs.sentinels import UNSET
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.validate_type_is_defined import (
    validate_type_is_defined,
)


def test_validate_type_is_defined_pass(sample_object_classes) -> None:
    """Tests that a defined _type attribute passes validation."""

    MyTestConstant, MyTestObject = sample_object_classes

    validate_type_is_defined(int, MyTestObject)


def test_validate_type_is_defined_raises_error(subtests, sample_object_classes) -> None:
    """Tests that UNSET _type attribute raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    assert_exception_function(
        subtests,
        validate_type_is_defined,
        invalid_params=(UNSET, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        value=UNSET,
        expected="A concrete type definition.",
        problem="The class 'MyTestObject' does not define the required '_type' attribute.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Define '_type' inside class 'MyTestObject'.",
            "The type must match the value structure represented by the class.",
            "Acceptable definitions:",
            "class MyTestObject(SimpleObject):",
            "    _type = int",
            "    _type = int | str",
            "    _type = (int, str)",
            "    ...",
        ),
        exception=AttributeError,
        verbose=False,
    )