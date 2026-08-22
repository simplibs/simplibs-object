from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.calculation.validations.raise_method_return_unvalide_outcome_type import (
    raise_method_return_unvalide_outcome_type,
)


def test_raise_method_return_unvalide_outcome_type(subtests) -> None:
    """Tests that returning invalid outcome type raises SimpleDefinitionError."""

    mock_self = Mock(__name__="MyObject")
    mock_func = Mock(__name__="_logic")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = mock_self
    mock_bound_method.__func__ = mock_func

    assert_exception_function(
        subtests,
        raise_method_return_unvalide_outcome_type,
        invalid_params=("invalid_return_value", dict, mock_bound_method),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_return_type",
        value="invalid_return_value",
        expected="dict",
        problem="Method '_logic' returned an invalid type 'str'.",
        context="Metadata validation for: MyObject._logic",
        how_to_fix=(
            "Inspect the method logic and ensure the returned value matches the expected type.",
            "Return value must match 'MyObject._type'.",
            "Modify the method so that it returns an instance of 'dict'.",
            "Or update the type definition to allow 'str'.",
            "Example:",
            "    @classmethod",
            "    def _logic(cls, ...) -> dict:",
            "        return ...  # Must be an instance of dict",
        ),
        exception=TypeError,
        verbose=False,
    )