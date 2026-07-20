import pytest
# Outers
from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.init_processors.names.validations.validate_class_name_is_ascii import (
    validate_class_name_is_ascii,
)
from simplibs.exception.testing import (
    assert_exception_function,
    assert_function_valid_input,
)


@pytest.mark.parametrize(
    "valid_name",
    ["ValidClassName", "Class123", "Contains_Underscores"]
)
def test_validate_class_name_is_ascii_happy_path(subtests, valid_name: str) -> None:
    """Verify that pure ASCII class names pass the validation guard without exceptions."""
    assert_function_valid_input(
        subtests,
        validate_class_name_is_ascii,
        valid_params=(valid_name,),
        verbose=False
    )


@pytest.mark.parametrize(
    "invalid_name",
    ["Třída", "Mesíc", "Ελληνικά", "CaféClass"]
)
def test_validate_class_name_is_ascii_invalid_inputs(subtests, invalid_name: str) -> None:
    """Verify that class names with non-ASCII characters trigger a properly formatted SimpleMetadataError."""
    assert_exception_function(
        subtests,
        validate_class_name_is_ascii,
        invalid_params=(invalid_name,),
        exception_type=SimpleMetadataError,
        value=invalid_name,
        label="Non-standard characters detected",
        expected="Strictly basic ASCII characters (A-Z, a-z, 0-9, _).",
        problem="The class name contains disallowed characters (localized diacritics or non-ASCII symbols).",
        context="Structural validation of dynamic class identifiers during metadata extraction.",
        how_to_fix=(
            "The class possesses an invalid name — it was likely generated dynamically with an invalid input string.",
            "Remove all accents, hooks, and diacritics from the class identifier (e.g., transform 'Měna' to 'Mena').",
            "Review the runtime blueprint definition layer or contact the system administrator.",
        ),
    )