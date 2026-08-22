from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.annotations_and_defaults.validations.validate_args_defaults import (
    validate_args_defaults,
)


def test_validate_args_defaults_pass() -> None:
    """Tests that matching positional defaults pass validation."""

    mock_func = Mock()
    mock_func.__defaults__ = (10, "default_str")
    mock_bound_method = Mock()
    mock_bound_method.__func__ = mock_func

    validate_args_defaults(
        expected_args_defaults=(10, "default_str"),
        expected_params=("arg1", "arg2"),
        bound_method=mock_bound_method,
        exception_info=("TestClass", "test_method", "Context"),
        expected_structure=("Blueprint",),
    )


def test_validate_args_defaults_raises_error(subtests) -> None:
    """Tests that mismatching positional defaults raise SimpleDefinitionError."""

    mock_func = Mock()
    mock_func.__defaults__ = (99,)
    mock_bound_method = Mock()
    mock_bound_method.__func__ = mock_func

    assert_exception_function(
        subtests,
        validate_args_defaults,
        invalid_params=(
            (10,),
            ("arg1",),
            mock_bound_method,
            ("TestClass", "test_method", "TestContext"),
            ("Expected structure line 1",),
        ),
        exception_type=SimpleDefinitionError,
        error_name="METHOD SIGNATURE ERROR",
        label="_args_default",
        expected="10",
        value=99,
        problem="Parameter 'arg1' has an incorrect default value.",
        context="TestContext",
        how_to_fix=(
            "Set the default value of 'arg1' to '10'.",
            "Or remove the default entirely; the framework will inject it automatically.",
            "Expected structure line 1",
        ),
        exception=ValueError,
        verbose=False,
    )