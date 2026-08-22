import pytest
from simplibs.sentinels import UNSET
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.tools.automate_creators._validations.validate_composite_has_not_default import (
    validate_composite_has_not_default,
)


def test_validate_composite_has_not_default_pass() -> None:
    """Tests that default=UNSET passes validation for composite definitions."""
    validate_composite_has_not_default("MyCompositeClass", UNSET)


@pytest.mark.parametrize("invalid_default", [10, "default_val", False, None, [1, 2, 3]])
def test_validate_composite_has_not_default_raises_error(subtests, invalid_default) -> None:
    """Tests that passing a default parameter to a composite definition raises SimpleRuntimeError."""
    class_name = "MyCompositeClass"

    assert_exception_function(
        subtests,
        validate_composite_has_not_default,
        invalid_params=(class_name, invalid_default),
        exception_type=SimpleRuntimeError,
        error_name="COMPOSITE DEFAULT CONFLICT ERROR",
        label="composite_default_conflict",
        value=invalid_default,
        expected="default=UNSET when creating a SimpleObject composite class",
        problem="Composite class 'MyCompositeClass' received a 'default' parameter, which is reserved for leaf constants.",
        context="Dynamic creator detected 'inners' tuple was provided for composite class 'MyCompositeClass'.",
        how_to_fix=(
            "SimpleObject composite values are dynamically derived from child 'inners' via 'logic' calculation.",
            "If this is a composite node: remove the 'default' argument.",
            "Required for composites: 'inners', 'logic'. Optional for composites: 'decompose', 'validate', 'value_type'.",
            "If this is a leaf constant: remove 'inners' and 'logic'. Constants require: 'default' (optional: 'validate', 'value_type').",
        ),
        exception=ValueError,
        verbose=False,
    )