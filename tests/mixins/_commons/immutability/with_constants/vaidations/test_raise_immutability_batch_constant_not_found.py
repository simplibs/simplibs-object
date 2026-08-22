from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_constants.vaidations.raise_immutability_batch_constant_not_found import (
    raise_immutability_batch_constant_not_found,
)


def test_raise_immutability_batch_constant_not_found(subtests) -> None:
    """Tests that raise_immutability_batch_constant_not_found raises SimpleRuntimeError."""

    class MyClass:
        _constant_names_set = {"a", "b"}

    dummy_instance = MyClass()

    assert_exception_function(
        subtests,
        raise_immutability_batch_constant_not_found,
        invalid_params=(dummy_instance, "non_existent_constant"),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="constant name",
        value="non_existent_constant",
        expected="Each (name, value) pair must refer to a valid constant.",
        problem=(
            "Constant 'non_existent_constant' does not exist in the instance. ",
            "Batch immutable update cannot continue.",
        ),
        context="Batch update attempted on instance 'MyClass'. Valid constants",
        how_to_fix=(
            "Ensure that every (name, value) tuple refers to a valid constant.",
            "Check the instance's `_constant_names_set` for available constants.",
            "If the name is meant to be a composite, use `with_composite` or `with_any` instead.",
            "Remove or correct the invalid constant name in the batch update.",
        ),
        exception=KeyError,
        verbose=False,
    )