from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.names.validations.validate_class_name_is_identifier import (
    validate_class_name_is_identifier,
)


def test_validate_class_name_is_identifier_pass() -> None:
    """Tests that a valid Python identifier passes validation."""

    validate_class_name_is_identifier("MyClass")
    validate_class_name_is_identifier("Class_123")


def test_validate_class_name_is_identifier_raises_error(subtests) -> None:
    """Tests that an invalid Python identifier raises SimpleDefinitionError."""

    invalid_class_name = "123Class"

    assert_exception_function(
        subtests,
        validate_class_name_is_identifier,
        invalid_params=(invalid_class_name,),
        exception_type=SimpleDefinitionError,
        error_name="CLASS NAME NOT IDENTIFIER",
        label="class name",
        value=invalid_class_name,
        expected="A name using only letters, digits, and underscores.",
        problem="The name '123Class' is not a valid Python identifier.",
        context="Identifier validation during metadata name processing.",
        how_to_fix=(
            "Remove spaces, hyphens, dots, or other special characters.",
            "Ensure the name does not start with a digit.",
            "If creating classes dynamically via type(name, ...), verify the name first.",
        ),
        exception=ValueError,
        verbose=False,
    )