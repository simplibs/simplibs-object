from typing import Any
# Outers
from ....SimpleConstant import SimpleConstant
from ....exceptions import SimpleRuntimeError


def validate_instance_is_simple_constant_base(
    instance: Any
) -> None:
    """Validates that the provided object is an instance of SimpleConstant or its subclasses.

    Args:
        instance: Candidate instance object to validate.

    Raises:
        SimpleRuntimeError: If instance is not a SimpleConstant subclass instance.
    """

    if isinstance(instance, SimpleConstant):
        return

    raise SimpleRuntimeError(
        error_name="INVALID INSTANCE TYPE ERROR",
        label="instance",
        expected="An instance inheriting from SimpleConstant or SimpleObject.",
        value=type(instance).__name__,
        problem=(
            "Provided instance does not derive from SimpleConstant.",
            "Random data fill operations require a Simple framework instance."
        ),
        context=(
            f"Received object: {instance!r}",
            f"Received type: '{type(instance).__name__}'",
        ),
        how_to_fix=(
            "Pass a valid SimpleConstant or SimpleObject instance to random_data_filler / randomize_value.",
            "Ensure the object was initialized via the Simple ecosystem base classes."
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# validate_instance_is_simple_constant_base

## Purpose
Validates that the `instance` argument passed to random data fillers is a valid `SimpleConstant` instance.

## Why this validation exists
Randomization algorithms inspect `.meta.is_constant`, `.meta.inners`, and assign to `.value`. 
Passing non-Simple objects would cause missing attribute errors deep in execution.
"""