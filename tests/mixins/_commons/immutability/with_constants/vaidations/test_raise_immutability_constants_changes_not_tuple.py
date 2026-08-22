from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_constants.vaidations.raise_immutability_constants_changes_not_tuple import (
    raise_immutability_constants_changes_not_tuple,
)


def test_raise_immutability_constants_changes_not_tuple(subtests) -> None:
    """Tests that raise_immutability_constants_changes_not_tuple raises SimpleRuntimeError."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    invalid_changes = ["a", 1]

    assert_exception_function(
        subtests,
        raise_immutability_constants_changes_not_tuple,
        invalid_params=(dummy_instance, invalid_changes),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY UPDATE ERROR",
        label="changes",
        value="list",
        expected="Tuple of (name, value) pairs or a single (name, value) tuple.",
        problem=(
            "Invalid type for `changes` argument in `with_constants`. ",
            "Immutable batch update requires a tuple-based structure.",
        ),
        context=(
            "Immutable constant batch update on instance 'MyClass'. ",
            "The `changes` parameter must be a tuple.",
        ),
        how_to_fix=(
            "Pass changes as a tuple: ((name, value), (name, value), ...).",
            "For a single change, use: (name, value) — it will be normalized internally.",
            "Do not use lists, dicts, or other container types for `changes`.",
        ),
        exception=TypeError,
        verbose=False,
    )