from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.validate_type_is_not_none import (
    validate_type_is_not_none,
)


def test_validate_type_is_not_none_pass(sample_object_classes) -> None:
    """Tests that a non-None _type attribute passes validation."""

    MyTestConstant, MyTestObject = sample_object_classes
    validate_type_is_not_none(int, MyTestObject)


def test_validate_type_is_not_none_raises_error(subtests, sample_object_classes) -> None:
    """Tests that setting _type to literal None raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    assert_exception_function(
        subtests,
        validate_type_is_not_none,
        invalid_params=(None, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        value=None,
        expected="A concrete type or a UnionType.",
        problem="The '_type' attribute is set to literal None.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Replace literal None with a real type.",
            "If you intended to allow absence of value, use NoneType instead.",
            "Literal None cannot serve as a structural type definition.",
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