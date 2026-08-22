import pytest
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.object_methods.validations.raise_duplicate_argument_error import (
    raise_duplicate_argument_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, param_name",
    [
        ("UserObject", "age"),
        ("CustomComposite", "value_list"),
    ],
)
def test_raise_duplicate_argument_error(
    subtests, class_name: str, param_name: str
) -> None:
    """Test that passing argument positionally AND by keyword raises SimpleRuntimeError."""

    dummy_cls = Mock()
    dummy_cls.__name__ = class_name

    assert_exception_function(
        subtests,
        raise_duplicate_argument_error,

        invalid_params=(dummy_cls, param_name),
        exception_type=SimpleRuntimeError,

        error_name="INVALID PARAMETERS",
        label=param_name,
        value=f"Positional and keyword argument for '{param_name}'",
        expected=f"Parameter '{param_name}' provided either positionally OR as a keyword",
        problem=(
            f"The parameter '{param_name}' was supplied twice when calling "
            f"'{class_name}.calculate_value': once as a positional argument and "
            f"once as a keyword argument."
        ),
        context=(
            f"During parameter processing for '{class_name}.calculate_value', "
            f"the system detected a duplicate argument definition."
        ),
        how_to_fix=(
            "Provide the parameter only once.",
            "If you prefer positional arguments, remove the keyword version.",
            "If you prefer keyword arguments, remove the positional version.",
            "Ensure that each inner element is mapped to exactly one argument.",
        ),
        exception=ValueError,

        verbose=False,
    )