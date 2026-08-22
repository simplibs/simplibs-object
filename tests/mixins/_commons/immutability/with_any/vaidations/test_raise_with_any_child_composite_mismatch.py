from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_any.vaidations.raise_with_any_child_composite_mismatch import (
    raise_with_any_child_composite_mismatch,
)


def test_raise_with_any_child_composite_mismatch(subtests) -> None:
    """Tests that raise_with_any_child_composite_mismatch raises SimpleRuntimeError with ValueError."""

    class MyClass:
        pass

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        raise_with_any_child_composite_mismatch,
        invalid_params=(dummy_instance, "child_comp", 10, 20),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY CHILD COMPOSITE ERROR",
        label="child composite mismatch",
        value=10,
        expected="Child composite 'child_comp' must match its recalculated value.",
        problem=(
            "Child composite 'child_comp' does not match the recalculated value.",
            "Provided value: 10",
            "Recalculated value: 20",
        ),
        context=(
            "Mixed update attempted on instance 'MyClass'.",
            "Child composites cannot be directly overridden when they depend on parent composites.",
        ),
        how_to_fix=(
            "Do not assign values to child composites directly.",
            "Update the corresponding root composite instead.",
            "Child composite values are derived automatically from parent composites.",
        ),
        exception=ValueError,
        verbose=False,
    )