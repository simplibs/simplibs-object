from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins._common_logic.immutability.with_constants.vaidations.validate_inner_tuple_has_length_two import (
    validate_inner_tuple_has_length_two,
)


def test_validate_inner_tuple_has_length_two_success() -> None:
    """Tests that valid 2-item tuple passes without error."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    validate_inner_tuple_has_length_two(dummy_instance, ("attr", 123))


def test_validate_inner_tuple_has_length_two_raises_error(subtests) -> None:
    """Tests that invalid length tuple raises SimpleRuntimeError."""

    class MyClass:
        pass

    dummy_instance = MyClass()
    invalid_tuple = ("attr", 123, "extra")

    assert_exception_function(
        subtests,
        validate_inner_tuple_has_length_two,
        invalid_params=(dummy_instance, invalid_tuple),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="change item length",
        value="length=3",
        expected="Tuple of exactly two items: (name, value).",
        problem=(
            "Invalid structure for change item. ",
            "Each change must be a 2‑item tuple representing (name, value).",
        ),
        context=(
            "Batch update attempted on instance 'MyClass'. ",
            "The provided tuple does not have exactly two items.",
        ),
        how_to_fix=(
            "Ensure each change is provided as a 2‑item tuple.",
            "Correct format: (name, value)",
            "Incorrect formats include: (name,), (name, value, extra), or any other size.",
        ),
        exception=ValueError,
        verbose=False,
    )