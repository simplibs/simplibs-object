import pytest
from unittest.mock import Mock

from simplibs.exception.testing import (
    assert_exception_function,
)
from simplibs.object._core.logic.constant_methods.validations.raise_missing_value_error import (
    raise_missing_value_error,
)
from simplibs.object.exceptions import SimpleRuntimeError


@pytest.mark.parametrize(
    "class_name, expected_type",
    [
        ("MyConstant", "int"),
        ("CustomObject", "str | int"),
    ],
)
def test_raise_missing_value_error(
    subtests, class_name: str, expected_type: str
) -> None:
    """Test that providing None raises SimpleRuntimeError with correct ecosystem details."""

    # Dummy mock class matching SimpleConstantProtocol structure
    dummy_cls = Mock()
    dummy_cls.__name__ = class_name
    dummy_cls.meta.value_type_name = expected_type

    assert_exception_function(
        subtests,
        raise_missing_value_error,

        invalid_params=(dummy_cls,),
        exception_type=SimpleRuntimeError,

        error_name="MISSING VALUE ERROR",
        label="value",
        value=None,
        expected=f"A valid instance of type '{expected_type}' (not None)",
        problem=f"The class '{class_name}' requires a concrete value, but received None.",
        context=(
            f"Normalization phase for '{class_name}' rejected a None value because "
            f"None is not permitted in the SimpleObject ecosystem."
        ),
        how_to_fix=(
            "Provide a valid value or an instance of the required type.",
            "If you want the system to automatically substitute the default value "
            "when None is provided, call the method with 'process_none=True'.",
        ),
        exception=ValueError,

        verbose=False,
    )