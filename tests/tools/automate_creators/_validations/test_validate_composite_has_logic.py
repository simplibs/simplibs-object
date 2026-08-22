import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_composite_has_logic import (
    validate_composite_has_logic,
)


@pytest.mark.parametrize("valid_logic", [lambda x: x, print, len])
def test_validate_composite_has_logic_pass(valid_logic) -> None:
    """Tests that valid non-None and non-UNSET logic callables pass validation."""
    validate_composite_has_logic("MyCompositeClass", valid_logic)


@pytest.mark.parametrize("invalid_logic", [UNSET, None])
def test_validate_composite_has_logic_raises_error(subtests, invalid_logic) -> None:
    """Tests that UNSET or None logic rules raise SimpleRuntimeError."""

    class_name = "MyCompositeClass"

    assert_exception_function(
        subtests,
        validate_composite_has_logic,
        invalid_params=(class_name, invalid_logic),
        exception_type=SimpleRuntimeError,
        error_name="COMPOSITE MISSING LOGIC ERROR",
        label="composite_missing_or_none_logic",
        value=invalid_logic,
        expected="A valid non-None and non-UNSET callable logic function (logic not in (UNSET, None))",
        problem=(
            f"Composite class 'MyCompositeClass' specifies 'inners' but is missing the required 'logic' "
            f"calculation rule (received: {invalid_logic!r})."
        ),
        context=(
            "Dynamic creator inferred composite mode for class 'MyCompositeClass' because 'inners' was provided, "
            "but a valid logic pipeline was not supplied."
        ),
        how_to_fix=(
            "SimpleObject composites must derive their value from inner child components via a 'logic' function.",
            "Provide a callable 'logic' function (or lambda) accepting parameters corresponding to inner snake_case names.",
            "Do not pass None or UNSET for 'logic' when defining composite objects.",
            "Required for composites: 'inners', 'logic'. Optional: 'decompose', 'validate', 'value_type'.",
            "If this is a leaf constant: remove 'inners' and provide a static 'default' value instead.",
        ),
        exception=ValueError,
        verbose=False,
    )