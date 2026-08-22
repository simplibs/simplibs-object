from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.classmethod.validations.validate_method_is_classmethod import (
    validate_method_is_classmethod,
)


def test_validate_method_is_classmethod_pass() -> None:
    """Tests that a @classmethod descriptor passes validation."""

    @classmethod
    def dummy_method(cls):
        pass

    validate_method_is_classmethod(
        raw_method=dummy_method,
        exception_info=("MyClass", "dummy_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_method_is_classmethod_raises_error(subtests) -> None:
    """Tests that non-classmethod attributes raise SimpleDefinitionError."""

    def plain_function(cls):
        pass

    exception_info = ("MyClass", "plain_function", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_method_is_classmethod,
        invalid_params=(plain_function, exception_info, expected_structure),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_method",
        value=plain_function,
        expected="A method decorated with '@classmethod'.",
        problem="'MyClass.plain_function' is not a classmethod.",
        context="TestContext",
        how_to_fix=(
            "Add '@classmethod' to 'plain_function'.",
            "Without this decorator, the system cannot bind the method correctly.",
            "Expected structure line 1",
        ),
        exception=TypeError,
        verbose=False,
    )