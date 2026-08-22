from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.params.validations.validate_method_has_exact_args_count import (
    validate_method_has_exact_args_count,
)


def test_validate_method_has_exact_args_count_pass() -> None:
    """Tests that matching argument counts pass validation."""

    validate_method_has_exact_args_count(
        expected_args_count=3,
        actual_args_count=3,
        exception_info=("MyClass", "my_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_method_has_exact_args_count_raises_error(subtests) -> None:
    """Tests that mismatching argument counts raise SimpleDefinitionError."""

    exception_info = ("MyClass", "my_method", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_method_has_exact_args_count,
        invalid_params=(3, 1, exception_info, expected_structure),
        exception_type=SimpleDefinitionError,
        error_name="METHOD SIGNATURE ERROR",
        label="_args_count",
        value=1,
        expected="3",
        problem="Incorrect number of positional arguments.",
        context="TestContext",
        how_to_fix=(
            "Ensure all required positional parameters are declared after 'cls'.",
            "Verify that the classmethod signature matches the expected framework definition.",
            "Expected structure line 1",
        ),
        exception=TypeError,
        verbose=False,
    )