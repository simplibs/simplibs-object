import pytest
from simplibs.object.exceptions import SimpleInitializationError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object._core.metadata.instance_builders.instance.validations.validate_param_is_bool import (
    validate_param_is_bool,
)


@pytest.mark.parametrize("valid_bool", [True, False])
def test_validate_param_is_bool_pass(valid_bool: bool) -> None:
    """Tests that boolean values pass validation."""

    validate_param_is_bool(valid_bool)


def test_validate_param_is_bool_raises_error(subtests) -> None:
    """Tests that non-boolean values raise SimpleInitializationError."""

    invalid_param = "True"

    assert_exception_function(
        subtests,
        validate_param_is_bool,
        invalid_params=(invalid_param,),
        exception_type=SimpleInitializationError,
        error_name="INVALID PARAMETER",
        label="param_not_bool",
        value=invalid_param,
        expected="Boolean value (True or False)",
        problem="Parameter is not bool. Received: 'True' (str).",
        context="create_instance(..., as_atom=...)",
        how_to_fix=(
            "Set the parameter to True or False.",
            "Example:",
            "    create_instance(MyClass, mixins=(), as_atom=True)",
        ),
        exception=TypeError,
        verbose=False,
    )