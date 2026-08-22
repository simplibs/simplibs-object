from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_constants.vaidations.validate_inner_tuple_is_tuple import (
    validate_inner_tuple_is_tuple,
)


def test_validate_inner_tuple_is_tuple_success() -> None:
    """Tests that a tuple passes validation without error."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    validate_inner_tuple_is_tuple(dummy_instance, ("attr", 123))


def test_validate_inner_tuple_is_tuple_raises_error(subtests) -> None:
    """Tests that non-tuple items raise SimpleRuntimeError."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    invalid_item = ["attr", 123]  # List instead of tuple

    assert_exception_function(
        subtests,
        validate_inner_tuple_is_tuple,
        invalid_params=(dummy_instance, invalid_item),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="change item",
        value="list",
        expected="Each change must be a tuple: (name, value).",
        problem=(
            "Invalid structure for change item. ",
            "Batch immutable update requires each item to be a tuple.",
        ),
        context=(
            "Batch update attempted on instance 'MyClass'. ",
            "The provided item is not a tuple.",
        ),
        how_to_fix=(
            "Ensure each change is provided as a tuple: (name, value).",
            "Example: ('age', 42)",
            "Do not use lists, dicts, or other container types.",
        ),
        exception=TypeError,
        verbose=False,
    )