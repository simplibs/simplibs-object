from unittest.mock import Mock
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.exception.testing.assert_exception_function import assert_exception_function
from simplibs.object.mixins.others.immutable._validations.raise_with_changes_input_not_dict import (
    raise_with_changes_input_not_dict,
)


def test_raise_with_changes_input_not_dict(subtests) -> None:
    """Tests that raise_with_changes_input_not_dict raises SimpleRuntimeError."""

    dummy_instance = Mock()
    type(dummy_instance).__name__ = "MyImmutableObj"

    invalid_value = ["width", 10]  # Neplatný vstup (list místo dict)

    assert_exception_function(
        subtests,
        raise_with_changes_input_not_dict,
        invalid_params=(dummy_instance, invalid_value),
        exception_type=SimpleRuntimeError,
        error_name="IMMUTABILITY UPDATE ERROR",
        label="changes_dict",
        value="['width', 10]",
        expected="A dictionary mapping constant names to new values.",
        problem=(
            "Invalid input provided to `with_changes`.",
            "The method expects a dictionary of constant updates.",
        ),
        context=(
            "Immutable update attempted on instance 'MyImmutableObj'.",
            "Provided value type: list",
        ),
        how_to_fix=(
            "Ensure that `changes_dict` is a dictionary.",
            "Example: {'width': 10, 'height': 20}",
            "For tuple-based updates, use `with_constants` instead.",
        ),
        exception=TypeError,
        verbose=False,
    )