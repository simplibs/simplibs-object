from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.classmethod.validations.validate_method_is_callable import (
    validate_method_is_callable,
)


def test_validate_method_is_callable_pass() -> None:
    """Tests that a callable object passes validation."""

    def dummy_function():
        pass

    validate_method_is_callable(
        raw_method=dummy_function,
        exception_info=("MyClass", "my_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_method_is_callable_raises_error(subtests) -> None:
    """Tests that non-callable raw attributes raise SimpleDefinitionError."""

    invalid_raw_method = "not_a_callable_string"
    exception_info = ("MyClass", "my_method", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_method_is_callable,
        invalid_params=(invalid_raw_method, exception_info, expected_structure),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_method",
        value=invalid_raw_method,
        expected="A callable classmethod.",
        problem="'MyClass.my_method' is not callable.",
        context="TestContext",
        how_to_fix=(
            "Ensure 'my_method' is defined as a function.",
            "Verify it was not overwritten by a data attribute.",
            "Expected structure line 1",
        ),
        exception=TypeError,
        verbose=False,
    )