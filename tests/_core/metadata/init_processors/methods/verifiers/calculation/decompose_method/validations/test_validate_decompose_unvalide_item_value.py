from unittest.mock import Mock
from simplibs.object.exceptions.SimpleDefinitionError import SimpleDefinitionError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.init_processors.methods.verifiers.calculation.decompose_method.validations.validate_decompose_unvalide_item_value import (
    validate_decompose_unvalide_item_value,
)


def test_validate_decompose_unvalide_item_value_pass() -> None:
    """Tests that matching value passes validation."""

    mock_bound_method = Mock()
    inner = Mock()
    inner.meta.default = "default_value"
    inners = (inner,)

    validate_decompose_unvalide_item_value(
        value="default_value",
        inner=inner,
        inners=inners,
        bound_method=mock_bound_method,
    )


def test_validate_decompose_unvalide_item_value_raises_error(subtests) -> None:
    """Tests that mismatched item value raises SimpleDefinitionError."""

    mock_self = Mock(__name__="MyObject")
    mock_func = Mock(__name__="_decompose")
    mock_bound_method = Mock()
    mock_bound_method.__self__ = mock_self
    mock_bound_method.__func__ = mock_func

    inner1 = Mock()
    inner1.meta.name_snake = "target_param"
    inner1.meta.default = "expected_str"

    inners = (inner1,)

    assert_exception_function(
        subtests,
        validate_decompose_unvalide_item_value,
        invalid_params=("wrong_str", inner1, inners, mock_bound_method),
        exception_type=SimpleDefinitionError,
        error_name="METHOD LOGIC ERROR",
        label="_decompose_item_value",
        value="wrong_str",
        expected="'expected_str'",
        problem="Item 'target_param' does not match its expected default value.",
        context="Metadata validation for: MyObject._decompose",
        how_to_fix=(
            "Ensure that 'target_param' is computed as ''expected_str''.",
            "Received value: ''wrong_str''.",
            "Verify that the returned tuple preserves the exact order defined in '_inners'.",
            "Expected order: target_param.",
            "Example based on default values:",
            "    return ('expected_str')",
        ),
        exception=ValueError,
        verbose=False,
    )