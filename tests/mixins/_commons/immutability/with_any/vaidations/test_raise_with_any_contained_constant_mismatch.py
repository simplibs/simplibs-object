from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_any.vaidations.raise_with_any_contained_constant_mismatch import (
    raise_with_any_contained_constant_mismatch,
)


def test_raise_with_any_contained_constant_mismatch(subtests) -> None:
    """Tests that raise_with_any_contained_constant_mismatch raises SimpleRuntimeError with ValueError."""

    class MyClass:
        pass

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        raise_with_any_contained_constant_mismatch,
        invalid_params=(dummy_instance, "contained_const", "user_val", "calc_val"),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY CONTAINED CONSTANT ERROR",
        label="contained constant mismatch",
        value="user_val",
        expected="Constant 'contained_const' must match its recalculated value.",
        problem=(
            "Contained constant 'contained_const' does not match the recalculated value.",
            "Provided value: 'user_val'",
            "Recalculated value: 'calc_val'",
        ),
        context=(
            "Mixed update attempted on instance 'MyClass'.",
            "Contained constants cannot override values derived from composite updates.",
        ),
        how_to_fix=(
            "Do not assign values to contained constants directly.",
            "Update the corresponding composite instead.",
            "Contained constants are derived automatically from composite values.",
        ),
        exception=ValueError,
        verbose=False,
    )