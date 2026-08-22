from typing import TYPE_CHECKING, NoReturn
# Outers
from ....exceptions import SimpleRuntimeError
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.instance import SimpleInstanceLike


def raise_random_data_filler_exhausted(
    instance: "SimpleInstanceLike",
    retries: int,
) -> NoReturn:
    """Raises a structured error when random data generation fails to produce a valid value after retry attempts."""

    instance_type_name = type(instance).__name__
    value_type_name = getattr(getattr(instance, "meta", None), "value_type", None)
    type_repr = getattr(value_type_name, "__name__", str(value_type_name))

    raise SimpleRuntimeError(
        error_name="RANDOM DATA FILLER EXHAUSTED ERROR",
        label="retries",
        expected=f"A valid random value generated within {retries} retry attempt(s).",
        value=f"Exhausted {retries} attempt(s)",
        problem=(
            f"Failed to generate a valid, distinct value for instance '{instance_type_name}'.",
            f"All {retries} attempt(s) failed setter validation or generated an identical value."
        ),
        context=(
            f"Target instance type: '{instance_type_name}'",
            f"Target value type hint: '{type_repr}'",
            f"Current instance value: {getattr(instance, 'value', None)!r}",
        ),
        how_to_fix=(
            "Increase the 'retries' parameter count in random_data_filler or randomize_value.",
            "Verify that a custom randomizer is registered for the target value type hint.",
            "Check if the instance setter or validation logic is overly restrictive."
        ),
        exception=RuntimeError,
    )


_DESIGN_NOTES = """
# raise_random_data_filler_exhausted

## Purpose
Raises a structured `SimpleRuntimeError` when random value generation exhausts all configured retry attempts 
without producing a value that passes instance validation.

## Why this validation exists
Fuzz testing relies on generating valid random inputs. If an instance validator consistently rejects generated values 
or if the generator only produces values equal to the current state, continuing execution indefinitely would result in a freeze.

## Execution context
Called at the end of `randomize_value` when the loop over `range(retries)` completes without returning.
"""