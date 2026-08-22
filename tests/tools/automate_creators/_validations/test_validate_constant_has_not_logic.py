import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_constant_has_not_logic import (
    validate_constant_has_not_logic,
)


def test_validate_constant_has_not_logic_pass() -> None:
    """Tests that logic=UNSET passes validation for constant definitions."""
    validate_constant_has_not_logic("MyConstantClass", UNSET)


@pytest.mark.parametrize("invalid_logic", [lambda x: x, print, "invalid_logic_callable"])
def test_validate_constant_has_not_logic_raises_error(subtests, invalid_logic) -> None:
    """Tests that passing a logic parameter to a constant definition raises SimpleRuntimeError."""
    class_name = "MyConstantClass"

    assert_exception_function(
        subtests,
        validate_constant_has_not_logic,
        invalid_params=(class_name, invalid_logic),
        exception_type=SimpleRuntimeError,
        error_name="CONSTANT LOGIC CONFLICT ERROR",
        label="constant_logic_conflict",
        value=invalid_logic,
        expected="logic=UNSET when creating a SimpleConstant class",
        problem="Constant class 'MyConstantClass' received a 'logic' parameter, which is reserved for composite objects.",
        context="Dynamic creator detected 'inners' was UNSET but received 'logic' for class 'MyConstantClass'.",
        how_to_fix=(
            "SimpleConstant leaf nodes store raw static values and do not support calculation rules ('logic').",
            "If this is a leaf node: remove the 'logic' argument. Allowed constant parameters: 'default', 'value_type', 'validate'.",
            "If this is a composite node: provide the 'inners' tuple specifying child component types alongside 'logic'.",
            "Required for composites: 'inners', 'logic'. Optional for composites: 'decompose', 'validate', 'value_type'.",
        ),
        exception=ValueError,
        verbose=False,
    )