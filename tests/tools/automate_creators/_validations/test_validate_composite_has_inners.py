import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_composite_has_inners import (
    validate_composite_has_inners,
)


@pytest.mark.parametrize("valid_inners", [(1,), ("inner_a", "inner_b"), ()])
def test_validate_composite_has_inners_pass(valid_inners) -> None:
    """Tests that valid non-None and non-UNSET inners pass validation."""
    validate_composite_has_inners("MyCompositeClass", valid_inners)


@pytest.mark.parametrize("invalid_inners", [UNSET, None])
def test_validate_composite_has_inners_raises_error(subtests, invalid_inners) -> None:
    """Tests that UNSET or None inners raise SimpleRuntimeError."""

    class_name = "MyCompositeClass"

    assert_exception_function(
        subtests,
        validate_composite_has_inners,
        invalid_params=(class_name, invalid_inners),
        exception_type=SimpleRuntimeError,
        error_name="COMPOSITE MISSING INNERS ERROR",
        label="composite_missing_or_none_inners",
        value=invalid_inners,
        expected="A valid non-empty tuple of inner component classes (inners not in (UNSET, None))",
        problem=(
            f"Attempted to create composite class 'MyCompositeClass' without specifying required 'inners' "
            f"child components (received: {invalid_inners!r})."
        ),
        context=(
            "Dynamic creator requires child component blueprints ('inners') to build "
            "a composite SimpleObject node tree."
        ),
        how_to_fix=(
            "Provide a tuple of child component blueprint classes for 'inners', e.g. inners=(ChildClassA, ChildClassB).",
            "Do not pass None or UNSET for 'inners' when defining composite objects.",
            "Required for composites: 'inners', 'logic'. Optional: 'decompose', 'validate', 'value_type'.",
            "If this is a leaf constant: remove 'logic' and provide a static 'default' value instead.",
        ),
        exception=ValueError,
        verbose=False,
    )