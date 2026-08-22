from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_constants.vaidations.validate_inner_tuple_name_is_str import (
    validate_inner_tuple_name_is_str,
)


def test_validate_inner_tuple_name_is_str_success() -> None:
    """Tests that tuple with string name passes validation without error."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    validate_inner_tuple_name_is_str(dummy_instance, ("valid_name", 123))


def test_validate_inner_tuple_name_is_str_raises_error(subtests) -> None:
    """Tests that tuple with non-string name raises SimpleRuntimeError."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    invalid_tuple = (123, "value")  # Integer as name

    assert_exception_function(
        subtests,
        validate_inner_tuple_name_is_str,
        invalid_params=(dummy_instance, invalid_tuple),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="change item name",
        value=123,
        expected="First element of tuple must be a string representing the node name.",
        problem=(
            "Invalid structure for change item. ",
            "The first element of each (name, value) tuple must be a string.",
        ),
        context=(
            "Batch update attempted on instance 'MyClass'. ",
            "The provided tuple has a non-string name element.",
        ),
        how_to_fix=(
            "Ensure the first element of each tuple is a string.",
            "Correct format: ('age', 42)",
            "Incorrect formats include: (123, 42), (None, 42), (object, 42).",
        ),
        exception=TypeError,
        verbose=False,
    )