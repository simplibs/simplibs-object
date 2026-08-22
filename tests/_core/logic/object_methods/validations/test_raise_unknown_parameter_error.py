import pytest
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.object_methods.validations.raise_unknown_parameter_error import (
    raise_unknown_parameter_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, unknown_params, expected_formatted",
    [
        ("UserComposite", ["foo"], "'foo'"),
        ("SettingsObject", ["invalid_opt", "unknown_key"], "'invalid_opt', 'unknown_key'"),
    ],
)
def test_raise_unknown_parameter_error(
    subtests, class_name: str, unknown_params: list[str], expected_formatted: str
) -> None:
    """Test that passing unknown kwargs to calculate_value raises SimpleRuntimeError."""

    dummy_cls = Mock()
    dummy_cls.__name__ = class_name

    assert_exception_function(
        subtests,
        raise_unknown_parameter_error,

        invalid_params=(dummy_cls, unknown_params),
        exception_type=SimpleRuntimeError,

        error_name="INVALID PARAMETERS",
        label="kwargs",
        value=expected_formatted,
        expected="Only parameters matching the inner elements of the composite",
        problem=(
            f"The class '{class_name}' does not define the following parameters: "
            f"{expected_formatted}."
        ),
        context=(
            f"During parameter processing for '{class_name}.calculate_value', "
            f"the system detected keyword arguments that do not correspond to "
            f"any inner element."
        ),
        how_to_fix=(
            "Remove the unknown keyword arguments.",
            "Ensure that each keyword argument matches the name of an inner element.",
            "Check the '_inners' definition of the class to see the valid parameter names.",
        ),
        exception=ValueError,

        verbose=False,
    )