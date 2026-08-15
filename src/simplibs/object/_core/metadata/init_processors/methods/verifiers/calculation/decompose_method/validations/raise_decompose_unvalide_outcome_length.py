from typing import TYPE_CHECKING
# Outers
from .........exceptions import SimpleDefinitionError
from ...._exceptions_helpers import exception_info_for_classmethod
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol


def raise_decompose_unvalide_outcome_length(
    calculate_default: tuple,
    inners: tuple,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Raises an exception when _decompose returns an incorrect number of items."""

    # 1. Extract diagnostic context
    _, method_name, context = exception_info_for_classmethod(bound_method)

    expected_count = len(inners)
    got_count = len(calculate_default)

    inner_names = tuple(inner.meta.name_snake for inner in inners)
    inner_defaults = tuple(repr(inner.meta.default) for inner in inners)

    # 2. Raise domain exception
    raise SimpleDefinitionError(
        error_name="METHOD LOGIC ERROR",
        label="_decompose_length",
        value=calculate_default,
        expected=repr(inner_names),
        problem=f"Expected {expected_count} items, received {got_count}.",
        context=context,
        how_to_fix=(
            "The '_decompose' method must return values matching the defined inner elements.",
            f"Ensure the return tuple contains exactly {expected_count} items.",
            f"Expected order: {', '.join(inner_names)}.",
            "Example based on default values:",
            f"    return ({', '.join(inner_defaults)})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_decompose_unvalide_outcome_length

## Purpose
Ensures that `_decompose` returns a tuple whose length matches the number of
inner components defined in the metadata (`_inners`).

## Behavior
1. Extracts diagnostic context using `exception_context_for_classmethod`.
2. Computes:
   - expected item count
   - actual item count
   - expected inner names
   - example default values
3. Raises a structured `SimpleDefinitionError` with clear remediation instructions.

## Notes
This validator is used exclusively inside `verify_decompose_outcome` and is the
first structural check before type/value validation.
"""