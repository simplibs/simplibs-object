from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.names.validations.validate_class_name_has_no_underscores import (
    validate_class_name_has_no_underscores,
)


def test_validate_class_name_has_no_underscores_pass() -> None:
    """Tests that a class name without underscores passes validation."""

    validate_class_name_has_no_underscores("MyClass")
    validate_class_name_has_no_underscores("Class123")


def test_validate_class_name_has_no_underscores_raises_error(subtests) -> None:
    """Tests that a class name containing underscores raises SimpleDefinitionError."""

    invalid_class_name = "My_Class"

    assert_exception_function(
        subtests,
        validate_class_name_has_no_underscores,
        invalid_params=(invalid_class_name,),
        exception_type=SimpleDefinitionError,
        error_name="CLASS NAME CONTAINS UNDERSCORE",
        label="class name",
        value=invalid_class_name,
        expected="Only alphanumeric characters (A–Z, a–z, 0–9).",
        problem="The name contains an underscore (_).",
        context="Underscore validation during metadata name processing.",
        how_to_fix=(
            "Remove all underscores from the class name.",
            "Use PascalCase (e.g., 'My_Class' → 'MyClass').",
            "Underscores are reserved for internal metadata and generated identifiers.",
        ),
        exception=ValueError,
        verbose=False,
    )