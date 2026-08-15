from typing import TYPE_CHECKING, NoReturn
# Outers
from ......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......_core.protocols.mixins.core_mixins import InfrastructureProtocol


def raise_immutability_batch_constant_not_found(
    instance: "InfrastructureProtocol",
    name: str,
) -> NoReturn:
    """
    Raises an error when a constant name inside a batch update does not
    exist in the instance's `_constant_names_set`.
    """

    # noinspection PyProtectedMember
    raise SimpleLogicError(
        error_name="IMMUTABILITY BATCH UPDATE ERROR",
        label="constant name",
        expected="Each (name, value) pair must refer to a valid constant.",
        value=name,
        problem=(
            f"Constant '{name}' does not exist in the instance. ",
            "Batch immutable update cannot continue."
        ),
        context=(
            f"Batch update attempted on instance '{type(instance).__name__}'. "
            f"Valid constants: {instance._constant_names_set}"
        ),
        how_to_fix=(
            "Ensure that every (name, value) tuple refers to a valid constant.",
            "Check the instance's `_constant_names_set` for available constants.",
            "If the name is meant to be a composite, use `with_composite` or `with_any` instead.",
            "Remove or correct the invalid constant name in the batch update.",
        ),
        exception=KeyError,
    )


_DESIGN_NOTES = """
# raise_immutability_batch_constant_not_found

## Purpose
Ensures that every `(name, value)` pair inside a batch constant update refers to
a valid constant.  
Batch updates must be structurally perfect — a single invalid name would break
the entire immutability pipeline.

This function provides a clear, structured diagnostic error when a constant name
is invalid.

## Architectural reasoning
`with_constants` processes multiple updates at once.  
For correctness:

- every name must be a valid constant,
- every constant must have metadata and validation logic,
- composite names must not appear in this pipeline.

If an invalid name appears:

- recalculation order becomes undefined,
- snapshot reconstruction becomes inconsistent,
- debugging becomes significantly harder.

Failing early prevents deeper structural corruption.

## Pipeline position
This function is used during step **4.3.3** of `with_constants`:

1. Extract `(inner_name, new_value)`.
2. Check whether `inner_name` is in `_constant_names_set`.
3. If not → raise this error immediately.
4. No further processing of this tuple is performed.

This guarantees that only valid constants enter the recalculation phase.

## Diagnostic value
The error message provides:

- the invalid constant name,
- the list of valid constants,
- the context of the batch update,
- actionable steps to fix the issue.

This makes the error friendly, actionable, and easy to understand.

## Notes
- This is a pure `raise_...` function: it performs no conditional logic.
- It is used exclusively by the `with_constants` pipeline.
- All batch constant updates must pass this check.
"""