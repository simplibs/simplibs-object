from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.calculation.decompose_method.validations.validate_decompose_unvalide_item_type import (
    validate_decompose_unvalide_item_type,
)


def test_validate_decompose_unvalide_item_type_pass() -> None:
    """Tests that matching type passes validation."""

    mock_bound_method = Mock()
    inner = Mock()
    inners = (inner,)

    validate_decompose_unvalide_item_type(
        value=100,
        expected_type=int,
        inner=inner,
        inners=inners,
        bound_method=mock_bound_method,
    )


def test_validate_decompose_unvalide_item_type_raises_error(subtests) -> None:
    """Tests that mismatched item type raises SimpleDefinitionError."""

    mock_self = Mock(__name__="MyObject")
    mock_func = Mock(__name__="_decompose")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = mock_self
    mock_bound_method.__func__ = mock_func

    inner1 = Mock()
    inner1.meta.name_snake = "target_param"
    inner1.meta.default = 42

    inners = (inner1,)

    assert_exception_function(
        subtests,
        validate_decompose_unvalide_item_type,
        invalid_params=("invalid_string_value", int, inner1, inners, mock_bound_method),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_decompose_item_type",
        value="invalid_string_value",
        expected="int",
        problem="Item 'target_param' does not match its expected type.",
        context="Metadata validation for: MyObject._decompose",
        how_to_fix=(
            "Ensure that 'target_param' is computed as an instance of 'int'.",
            "Received type: 'str'.",
            "Verify that the returned tuple preserves the exact order defined in '_inners'.",
            "Expected order: target_param.",
            "Example based on default values:",
            "    return (42)",
        ),
        exception=TypeError,
        verbose=False,
    )