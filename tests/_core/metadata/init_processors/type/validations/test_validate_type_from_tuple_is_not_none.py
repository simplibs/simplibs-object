from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.validate_type_from_tuple_is_not_none import (
    validate_type_from_tuple_is_not_none,
)


def test_validate_type_from_tuple_is_not_none_pass(sample_object_classes) -> None:
    """Tests that a non-None type inside a tuple passes validation."""

    MyTestConstant, MyTestObject = sample_object_classes

    validate_type_from_tuple_is_not_none(int, (int, str), MyTestObject)


def test_validate_type_from_tuple_is_not_none_raises_error(subtests, sample_object_classes) -> None:
    """Tests that a literal None inside a type tuple raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    type_tuple = (int, None)

    assert_exception_function(
        subtests,
        validate_type_from_tuple_is_not_none,
        invalid_params=(None, type_tuple, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        value=type_tuple,
        expected="A real type or class reference.",
        problem="The '_type' tuple contains a literal None value.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Replace literal None with a real type.",
            "If absence of value is intended, use NoneType instead.",
            "Literal None cannot be part of a type tuple.",
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