import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_constant_has_not_decompose import (
    validate_constant_has_not_decompose,
)


def test_validate_constant_has_not_decompose_pass() -> None:
    """Tests that decompose=UNSET passes validation for constant definitions."""
    validate_constant_has_not_decompose("MyConstantClass", UNSET)


@pytest.mark.parametrize("invalid_decompose", [lambda val: (val,), print, "invalid_decompose_handler"])
def test_validate_constant_has_not_decompose_raises_error(subtests, invalid_decompose) -> None:
    """Tests that passing a decompose parameter to a constant definition raises SimpleRuntimeError."""
    class_name = "MyConstantClass"

    assert_exception_function(
        subtests,
        validate_constant_has_not_decompose,
        invalid_params=(class_name, invalid_decompose),
        exception_type=SimpleRuntimeError,
        error_name="CONSTANT DECOMPOSE CONFLICT ERROR",
        label="constant_decompose_conflict",
        value=invalid_decompose,
        expected="decompose=UNSET when creating a SimpleConstant class",
        problem="Constant class 'MyConstantClass' received a 'decompose' parameter, which is reserved for composite objects.",
        context="Dynamic creator detected 'inners' was UNSET but received 'decompose' for class 'MyConstantClass'.",
        how_to_fix=(
            "SimpleConstant leaf nodes cannot be decomposed into inner children.",
            "If this is a leaf node: remove the 'decompose' argument. Allowed constant parameters: 'default', 'value_type', 'validate'.",
            "If this is a composite node: provide the 'inners' tuple specifying child component types.",
            "Required for composites: 'inners', 'logic'. Optional for composites: 'decompose', 'validate', 'value_type'.",
        ),
        exception=ValueError,
        verbose=False,
    )