import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_constant_has_default import (
    validate_constant_has_default,
)


@pytest.mark.parametrize("valid_default", [0, "", False, 123.45, (1, 2)])
def test_validate_constant_has_default_pass(valid_default) -> None:
    """Tests that valid non-None and non-UNSET default values pass validation."""
    validate_constant_has_default("MyConstantClass", valid_default)


@pytest.mark.parametrize("invalid_default", [UNSET, None])
def test_validate_constant_has_default_raises_error(subtests, invalid_default) -> None:
    """Tests that UNSET or None default values raise SimpleRuntimeError."""

    class_name = "MyConstantClass"

    assert_exception_function(
        subtests,
        validate_constant_has_default,
        invalid_params=(class_name, invalid_default),
        exception_type=SimpleRuntimeError,
        error_name="INVALID CONSTANT DEFAULT ERROR",
        label="constant_missing_or_none_default",
        value=invalid_default,
        expected="A valid non-UNSET and non-None default value (default not in (UNSET, None))",
        problem=(
            f"Attempted to create constant class 'MyConstantClass' with an invalid default value ({invalid_default!r}). ",
            "Constant default values cannot be UNSET or None.",
        ),
        context=(
            "Dynamic creator requires a concrete non-None default value for constant 'MyConstantClass' ",
            "to perform type inference and compute composite default values across node trees.",
        ),
        how_to_fix=(
            "Provide a concrete initial value for 'default' (e.g. 0, '', False, or a specific domain object).",
            "Do not use None as a default value — Simple framework trees rely on non-None defaults to derive composite logic.",
            "Supported optional parameters for constants: 'value_type', 'validate'.",
            "If you intended to create a SimpleObject (composite node): provide 'inners' tuple and 'logic' callable instead.",
        ),
        exception=ValueError,
        verbose=False,
    )