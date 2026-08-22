import pytest
from simplibs.object.exceptions import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_class_name_is_str import (
    validate_class_name_is_str,
)


@pytest.mark.parametrize("valid_name", ["MyConstant", "CustomClass", "A"])
def test_validate_class_name_is_str_pass(valid_name: str) -> None:
    """Tests that valid non-empty string class names pass validation."""
    validate_class_name_is_str(valid_name)


def test_validate_class_name_is_str_raises_error(subtests) -> None:
    """Tests that invalid class names raise SimpleDefinitionError."""

    invalid_class_name = 123  # Int místo str

    assert_exception_function(
        subtests,
        validate_class_name_is_str,
        invalid_params=(invalid_class_name,),
        exception_type=SimpleDefinitionError,
        error_name="INVALID CLASS NAME ERROR",
        label="class_name_is_not_str",
        value="int",
        expected="A non-empty string for class name definition",
        problem="Provided class name must be a non-empty string. Received type 'int'.",
        context="Attempted to dynamically generate a class blueprint, but 'class_name' validation failed.",
        how_to_fix=(
            "Pass a valid string for 'class_name', e.g. class_name='MyCustomConstant'.",
            "Ensure class_name is not empty or whitespace-only.",
        ),
        exception=TypeError,
        verbose=False,
    )