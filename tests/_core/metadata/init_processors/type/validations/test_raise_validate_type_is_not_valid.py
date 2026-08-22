from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.type.validations.raise_validate_type_is_not_valid import (
    raise_validate_type_is_not_valid,
)


def test_raise_validate_type_is_not_valid(subtests, sample_object_classes) -> None:
    """Tests that raise_validate_type_is_not_valid raises SimpleDefinitionError."""

    MyTestConstant, MyTestObject = sample_object_classes

    invalid_value = "unrecognized_string_type"

    assert_exception_function(
        subtests,
        raise_validate_type_is_not_valid,
        invalid_params=(invalid_value, MyTestObject),
        exception_type=SimpleDefinitionError,
        error_name="INVALID TYPE DEFINITION",
        label="_type",
        value=invalid_value,
        expected="A type, UnionType, or flat tuple of types.",
        problem="The '_type' attribute contains an unrecognized value.",
        context="Metadata validation for: MyTestObject._type",
        how_to_fix=(
            "Replace the value with a real type or a tuple of types.",
            "Do not use strings, instances, or nested containers.",
            "Ensure the definition matches the actual value structure.",
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