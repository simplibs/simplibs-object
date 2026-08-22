from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.params.validations.validate_method_not_use_param_placeholders import (
    validate_method_not_use_param_placeholders,
)


def test_validate_method_not_use_param_placeholders_pass() -> None:
    """Tests that signatures without *args and **kwargs pass validation."""

    validate_method_not_use_param_placeholders(
        has_varargs=False,
        has_varkwargs=False,
        exception_info=("MyClass", "my_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_method_not_use_param_placeholders_raises_error(subtests) -> None:
    """Tests that signatures using *args or **kwargs raise SimpleDefinitionError."""

    exception_info = ("MyClass", "my_method", "TestContext")
    expected_structure = ("Expected structure line 1",)

    assert_exception_function(
        subtests,
        validate_method_not_use_param_placeholders,
        invalid_params=(True, True, exception_info, expected_structure),
        exception_type=SimpleDefinitionError,
        error_name="METHOD SIGNATURE ERROR",
        label="_params",
        value="*args, **kwargs",
        expected="Explicitly named parameters.",
        problem="'MyClass.my_method' uses prohibited placeholders: *args, **kwargs.",
        context="TestContext",
        how_to_fix=(
            "Remove '*args, **kwargs' from the method signature.",
            "Declare each parameter explicitly by its exact semantic name.",
            "Expected structure line 1",
        ),
        exception=TypeError,
        verbose=False,
    )