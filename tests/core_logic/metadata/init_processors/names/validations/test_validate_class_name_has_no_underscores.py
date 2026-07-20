import pytest
# Outers
from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.init_processors.names.validations.validate_class_name_has_no_underscores import (
    validate_class_name_has_no_underscores,
)
from simplibs.exception.testing import (
    assert_exception_function,
    assert_function_valid_input,
)


@pytest.mark.parametrize(
    "valid_name",
    ["ValidClassName", "Class123", "PascalCaseEverywhere"]
)
def test_validate_class_name_has_no_underscores_happy_path(subtests, valid_name: str) -> None:
    """Verify that class names without any underscores pass the validation guard without exceptions."""
    assert_function_valid_input(
        subtests,
        validate_class_name_has_no_underscores,
        valid_params=(valid_name,),
        verbose=False
    )


@pytest.mark.parametrize(
    "invalid_name",
    ["My_Class", "_LeadingUnderscore", "TrailingUnderscore_", "__DoubleUnderscore__"]
)
def test_validate_class_name_has_no_underscores_invalid_inputs(subtests, invalid_name: str) -> None:
    """Verify that class names containing underscores trigger a properly formatted SimpleMetadataError."""
    assert_exception_function(
        subtests,
        validate_class_name_has_no_underscores,
        invalid_params=(invalid_name,),
        exception_type=SimpleMetadataError,
        value=invalid_name,
        label="Invalid character in name",
        expected="Exclusively alphanumeric characters (A-Z, a-z, 0-9).",
        problem="The class name contains an underscore (_), which is strictly prohibited within the SimpleObject architecture.",
        context="Structural validation of dynamic class identifiers during metadata extraction.",
        how_to_fix=(
            "Remove all underscores from the class name string.",
            "Example: Convert 'My_Class' to 'MyClass' (adhere strictly to PascalCase convention).",
            "Underscores are reserved for the framework's internal metadata derivation layers and generated identifiers.",
        ),
    )