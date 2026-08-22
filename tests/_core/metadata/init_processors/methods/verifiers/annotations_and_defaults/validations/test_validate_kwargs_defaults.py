from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.annotations_and_defaults.validations.validate_kwargs_defaults import (
    validate_kwargs_defaults,
)


def test_validate_kwargs_defaults_pass() -> None:
    """Tests that matching keyword-only defaults pass validation."""

    mock_func = Mock()
    mock_func.__kwdefaults__ = {"option": True}
    mock_bound_method = Mock()
    mock_bound_method.__func__ = mock_func

    validate_kwargs_defaults(
        expected_kwargs_defaults={"option": True},
        bound_method=mock_bound_method,
        exception_info=("TestClass", "test_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_kwargs_defaults_raises_error(subtests) -> None:
    """Tests that mismatching keyword-only defaults raise SimpleDefinitionError."""

    mock_func = Mock()
    mock_func.__kwdefaults__ = {"option": False}
    mock_bound_method = Mock()
    mock_bound_method.__func__ = mock_func

    assert_exception_function(
        subtests,
        validate_kwargs_defaults,
        invalid_params=(
            {"option": True},
            mock_bound_method,
            ("TestClass", "test_method", "TestContext"),
            ("Expected structure line 1",),
        ),
        exception_type=SimpleDefinitionError,
        error_name="METHOD SIGNATURE ERROR",
        label="_kwargs_default",
        expected="True",
        value=False,
        problem="Parameter 'option' has an incorrect default value.",
        context="TestContext",
        how_to_fix=(
            "Set the default value of 'option' to 'True'.",
            "Or remove the default entirely; the framework will inject it automatically.",
            "Expected structure line 1",
        ),
        exception=ValueError,
        verbose=False,
    )