from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.calculation.decompose_method.validations.raise_decompose_unvalide_outcome_length import (
    raise_decompose_unvalide_outcome_length,
)


def test_raise_decompose_unvalide_outcome_length(subtests) -> None:
    """Tests that incorrect return tuple length from _decompose raises SimpleDefinitionError."""

    # Mock bound_method
    mock_self = Mock(__name__="MyObject")
    mock_func = Mock(__name__="_decompose")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = mock_self
    mock_bound_method.__func__ = mock_func

    # Mock inners
    inner1 = Mock()
    inner1.meta.name_snake = "first_param"
    inner1.meta.default = 10

    inner2 = Mock()
    inner2.meta.name_snake = "second_param"
    inner2.meta.default = "hello"

    inners = (inner1, inner2)
    calculate_default = (10,)  # Length 1 instead of expected 2

    assert_exception_function(
        subtests,
        raise_decompose_unvalide_outcome_length,
        invalid_params=(calculate_default, inners, mock_bound_method),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_decompose_length",
        value=calculate_default,
        expected="('first_param', 'second_param')",
        problem="Expected 2 items, received 1.",
        context="Metadata validation for: MyObject._decompose",
        how_to_fix=(
            "The '_decompose' method must return values matching the defined inner elements.",
            "Ensure the return tuple contains exactly 2 items.",
            "Expected order: first_param, second_param.",
            "Example based on default values:",
            "    return (10, 'hello')",
        ),
        exception=ValueError,
        verbose=False,
    )