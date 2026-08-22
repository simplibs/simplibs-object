from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.names.validations.validate_class_name_is_ascii import (
    validate_class_name_is_ascii,
)


def test_validate_class_name_is_ascii_pass() -> None:
    """Tests that a purely ASCII class name passes validation."""

    validate_class_name_is_ascii("MyClass")
    validate_class_name_is_ascii("Class_123")


def test_validate_class_name_is_ascii_raises_error(subtests) -> None:
    """Tests that a class name containing non-ASCII characters raises SimpleDefinitionError."""

    invalid_class_name = "Třída"

    assert_exception_function(
        subtests,
        validate_class_name_is_ascii,
        invalid_params=(invalid_class_name,),
        exception_type=SimpleDefinitionError,
        error_name="CLASS NAME NOT ASCII",
        label="class name",
        value=invalid_class_name,
        expected="Only basic ASCII characters (A–Z, a–z, 0–9, _).",
        problem="The name contains non-ASCII characters.",
        context="ASCII validation during metadata name processing.",
        how_to_fix=(
            "Remove accents, hooks, and diacritics.",
            "Convert localized letters to plain ASCII (e.g., 'Měna' → 'Mena').",
            "If the name was created dynamically, verify the input string first.",
        ),
        exception=ValueError,
        verbose=False,
    )