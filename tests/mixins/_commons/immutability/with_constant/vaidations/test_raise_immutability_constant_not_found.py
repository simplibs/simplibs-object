from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_constant.vaidations.raise_immutability_constant_not_found import (
    raise_immutability_constant_not_found,
)


def test_raise_immutability_constant_not_found(subtests) -> None:
    """Tests that raise_immutability_constant_not_found raises SimpleRuntimeError with KeyError exception type."""

    class MyClass:
        _constant_names_set = {"const_a", "const_b"}

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        raise_immutability_constant_not_found,
        invalid_params=(dummy_instance, "missing_constant"),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY UPDATE ERROR",
        label="constant name",
        value="missing_constant",
        expected="Name must refer to a valid constant defined in the instance.",
        problem=(
            "Constant 'missing_constant' does not exist in the instance. ",
            "Immutable update cannot be applied.",
        ),
        context=(
            "Immutable update attempted on instance 'MyClass'.",
        ),
        how_to_fix=(
            "Ensure that the provided name refers to a valid constant.",
            "Check the instance's `_constant_names_set` for available constants.",
            "If the name is meant to be a composite, use `with_composite` instead.",
        ),
        exception=KeyError,
        verbose=False,
    )