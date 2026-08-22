from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_any.vaidations.raise_with_any_changes_is_not_tuple import (
    raise_with_any_changes_is_not_tuple,
)


def test_raise_with_any_changes_is_not_tuple(subtests) -> None:
    """Tests that raise_with_any_changes_is_not_tuple raises SimpleRuntimeError with TypeError."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    invalid_changes = ["const_a", 10]

    assert_exception_function(
        subtests,
        raise_with_any_changes_is_not_tuple,
        invalid_params=(dummy_instance, invalid_changes),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY UPDATE ERROR",
        label="changes",
        value="list",
        expected="Tuple of (name, value) pairs or a single (name, value) tuple.",
        problem=(
            "Invalid type for `changes` argument in with_any.",
            "Mixed immutable update requires a tuple-based structure.",
        ),
        context=(
            "Mixed update attempted on instance 'MyClass'.",
            "The provided `changes` value is not a tuple.",
        ),
        how_to_fix=(
            "Pass changes as a tuple: ((name, value), (name, value), ...).",
            "For a single change, use: (name, value).",
            "Do not use lists, dicts, or other container types.",
        ),
        exception=TypeError,
        verbose=False,
    )