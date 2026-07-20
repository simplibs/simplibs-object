import pytest
# Outers
from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.init_processors.names.validations.validate_class_name_is_identifier import (
    validate_class_name_is_identifier,
)
from simplibs.exception.testing import (
    assert_exception_function,
    assert_function_valid_input,
)


@pytest.mark.parametrize(
    "valid_name",
    ["ValidClassName", "WithDiacriticsČeština", "Contains_Underscores"]
)
def test_validate_class_name_is_identifier_happy_path(subtests, valid_name: str) -> None:
    """Verify that valid Python identifiers pass the validation guard without exceptions."""
    assert_function_valid_input(
        subtests,
        validate_class_name_is_identifier,
        valid_params=(valid_name,),
        verbose=False
    )


@pytest.mark.parametrize(
    "invalid_name",
    ["123Class", "My-Class", "My Class", "My.Class"]
)
def test_validate_class_name_is_identifier_invalid_inputs(subtests, invalid_name: str) -> None:
    """Verify that invalid Python identifiers trigger a properly formatted SimpleMetadataError."""
    assert_exception_function(
        subtests,
        validate_class_name_is_identifier,
        invalid_params=(invalid_name,),
        exception_type=SimpleMetadataError,
        value=invalid_name,
        label="Invalid Python name",
        expected="A valid identifier starting with a letter or underscore, containing only alphanumeric characters and underscores.",
        problem="The class name '",
        context="Structural validation of dynamic class identifiers during metadata extraction.",
        how_to_fix=(
            "Ensure the class name does not contain spaces, dashes, or dots.",
            "The name must not begin with a digit.",
            "When creating classes dynamically via type(name, ...), verify that the 'name' parameter complies with Python identifier rules.",
        ),
    )