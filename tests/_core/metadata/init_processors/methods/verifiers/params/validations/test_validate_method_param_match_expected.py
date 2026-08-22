from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.params.validations.validate_method_param_match_expected import (
    validate_method_param_match_expected,
)


def test_validate_method_param_match_expected_pass() -> None:
    """Tests that matching parameter tuples pass validation."""

    method_params = ("cls", "arg1", "arg2")
    expected_params = ("cls", "arg1", "arg2")

    validate_method_param_match_expected(
        method_params=method_params,
        expected_params=expected_params,
        exception_info=("MyClass", "my_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_method_param_match_expected_raises_error(subtests) -> None:
    """Tests that mismatched parameter tuples raise SimpleDefinitionError."""

    method_params = ("cls", "wrong_arg")
    expected_params = ("cls", "expected_arg")

    exception_info = ("MyClass", "my_method", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_method_param_match_expected,
        invalid_params=(method_params, expected_params, exception_info, expected_structure),
        exception_type=SimpleDefinitionError,
        error_name="METHOD SIGNATURE ERROR",
        label="_params",
        value=method_params,
        expected="('cls', 'expected_arg')",
        problem="Parameter names or their order do not match the expected signature.",
        context="TestContext",
        how_to_fix=(
            "Adjust the method signature to match the expected parameter layout.",
            "The first parameter must always be 'cls'.",
            "All other parameters must match the snake_case names of '_inners' components.",
            "Expected structure line 1",
        ),
        exception=TypeError,
        verbose=False,
    )