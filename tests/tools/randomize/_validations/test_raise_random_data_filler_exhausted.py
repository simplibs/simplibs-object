import pytest
from typing import Any
from unittest.mock import Mock
from simplibs.exception.testing import assert_exception_function
from simplibs.object.tools.randomize._validations.raise_random_data_filler_exhausted import (
    raise_random_data_filler_exhausted,
)
from simplibs.object.exceptions import SimpleRuntimeError


class DummyInstance:
    """Dummy class to simulate an instance within tests."""

    def __init__(self, value: Any = None, value_type: Any = None) -> None:
        self.value = value
        self.meta = Mock(value_type=value_type)


@pytest.mark.parametrize(
    "retries, instance_val, value_type_hint",
    [
        (5, 42, int),
        (10, "test_string", str),
        (3, None, type("CustomType", (), {})),
    ],
)
def test_raise_random_data_filler_exhausted(
    subtests, retries: int, instance_val: Any, value_type_hint: Any
) -> None:
    """Test that exhausting filler retry attempts raises SimpleRuntimeError with structured context and remediation advice."""
    dummy_instance = DummyInstance(value=instance_val, value_type=value_type_hint)
    instance_type_name = type(dummy_instance).__name__
    type_repr = getattr(value_type_hint, "__name__", str(value_type_hint))

    assert_exception_function(
        subtests,
        raise_random_data_filler_exhausted,
        invalid_params=(dummy_instance, retries),
        exception_type=SimpleRuntimeError,
        error_name="RANDOM DATA FILLER EXHAUSTED ERROR",
        label="retries",
        expected=f"A valid random value generated within {retries} retry attempt(s).",
        value=f"Exhausted {retries} attempt(s)",
        problem=(
            f"Failed to generate a valid, distinct value for instance '{instance_type_name}'.",
            f"All {retries} attempt(s) failed setter validation or generated an identical value.",
        ),
        context=(
            f"Target instance type: '{instance_type_name}'",
            f"Target value type hint: '{type_repr}'",
            f"Current instance value: {instance_val!r}",
        ),
        how_to_fix=(
            "Increase the 'retries' parameter count in random_data_filler or randomize_value.",
            "Verify that a custom randomizer is registered for the target value type hint.",
            "Check if the instance setter or validation logic is overly restrictive.",
        ),
        exception=RuntimeError,
        verbose=False,
    )