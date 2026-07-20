from typing import Union
import pytest
# Outers
from simplibs.object.exceptions import SimpleMetadataError
from simplibs.object._core_logic.metadata.init_processors.attributes.default.validations.constant.validate_default_matches_annotation import (
    validate_default_matches_annotation,
)
from simplibs.exception.testing import (
    assert_exception_function,
    assert_function_valid_input,
)


class MockSimpleObject:
    """Mock class mimicking a SimpleObject structure for metadata extraction."""
    pass


@pytest.mark.parametrize(
    "default_value, expected_type",
    [
        (42, int),
        ("Hello", str),
        (3.14, float),
        (42, Union[int, str]),
        ("World", Union[int, str]),
    ]
)
def test_validate_default_matches_annotation_happy_path(
    subtests,
    default_value: object,
    expected_type: object
) -> None:
    """Verify that type-compliant default values pass the validation guard without exceptions."""
    assert_function_valid_input(
        subtests,
        validate_default_matches_annotation,
        valid_params=(default_value, expected_type, MockSimpleObject),
        verbose=False
    )


@pytest.mark.parametrize(
    "default_value, expected_type",
    [
        ("NotAnInt", int),
        (42, str),
        (3.14, int),
        ([1, 2, 3], Union[int, str]),
    ]
)
def test_validate_default_matches_annotation_invalid_inputs(
    subtests,
    default_value: object,
    expected_type: object
) -> None:
    """Verify that type mismatches between default and annotation trigger a properly formatted SimpleMetadataError."""
    assert_exception_function(
        subtests,
        validate_default_matches_annotation,
        invalid_params=(default_value, expected_type, MockSimpleObject),
        exception_type=SimpleMetadataError,
        value=default_value,
        label="Type mismatch for default value",
        expected="A value conforming to the defined type: ",
        problem="The assigned default value does not match the declared type annotation.",
        context="MockSimpleObject",
        how_to_fix=(
            "Change the '_default' value to strictly match the '",
            "Alternatively, expand or modify the '_type' definition to encompass the current value's type.",
            "For a constant leaf structure (SimpleConstant), a valid, type-compliant '_default' is mandatory.",
        ),
    )