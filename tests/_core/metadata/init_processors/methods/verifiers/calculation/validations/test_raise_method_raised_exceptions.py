from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.calculation.validations.raise_method_raised_exceptions import (
    raise_method_raised_exceptions,
)


def test_raise_method_raised_exceptions(subtests) -> None:
    """Tests that intercepted dry-run exception is repackaged into SimpleDefinitionError."""

    mock_self = Mock(__name__="MyObject")
    mock_func = Mock(__name__="_logic")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = mock_self
    mock_bound_method.__func__ = mock_func

    root_exception = ZeroDivisionError("division by zero")

    assert_exception_function(
        subtests,
        raise_method_raised_exceptions,
        invalid_params=(root_exception, mock_bound_method),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_exception",
        expected="Method execution without raising exceptions.",
        problem="An unexpected error occurred during dry-run execution.",
        context="Metadata validation for: MyObject._logic",
        how_to_fix=(
            "Inspect the internal logic of '_logic'.",
            "Verify correct handling of default values and input parameters.",
            "See the intercepted exception below for the exact root cause.",
        ),
        exception=root_exception,
        verbose=False,
    )