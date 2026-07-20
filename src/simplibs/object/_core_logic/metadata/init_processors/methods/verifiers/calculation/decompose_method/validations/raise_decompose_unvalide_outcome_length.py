from typing import TYPE_CHECKING
# Outers
from .........exceptions import SimpleMetadataError
from ...._exceptions_helpers import exception_context_for_classmethod
# Annotations
if TYPE_CHECKING:
    from .........protocols.methods import ClassMethodProtocol


def raise_decompose_unvalide_outcome_length(
    calculate_default: tuple,
    inners: tuple,
    bound_method: "ClassMethodProtocol",
) -> None:
    """Raises an exception when the _decompose method returns an incorrect number of values.

    Raises:
        SimpleMetadataError: Always, as this is a dedicated exception raiser.
    """

    # 0. Exception condition boundary
    # if len(calculate_default) != len(inners):

    # 1. Compute dynamic diagnostic variables
    _, _, context = exception_context_for_classmethod(bound_method)
    expected_count = len(inners)
    got_count = len(calculate_default)
    inner_names_tuple = tuple(inner.meta.name_snake for inner in inners)
    inner_values_tuple = tuple(repr(inner.meta.default) for inner in inners)

    # 2. Raise domain exception with full packed diagnostic payload
    raise SimpleMetadataError(
        error_name="METHOD LOGIC ERROR",
        label="Incorrect number of returned values",
        expected=f"{repr(inner_names_tuple)} (tuple)",
        value=calculate_default,
        problem=f"Expected item count: {expected_count}, received item count: {got_count}.",
        context=context,
        how_to_fix=(
            "The '_decompose' method must return values matching the defined inner elements.",
            f"Modify the return value of '_decompose' to contain exactly {expected_count} items.",
            f"Expected item order: '{', '.join(inner_names_tuple)}'.",
            "Example based on default values from inners:",
            f"    return ({', '.join(inner_values_tuple)})"
        ),
        exception=ValueError
    )


_DESIGN_NOTES = """
# raise_decompose_unvalide_outcome_length

## Purpose
Acts as a dedicated panic endpoint when a custom `_decompose` structural method returns a tuple whose length mismatches the framework's compiled inner property configuration. It isolates complex diagnostic string building out of the primary test-run execution path.

## Diagnostic Layout & Formatting
1. **Dynamic Reflection Mapping**: Uses generator expressions cast to tuples to map internal `inner.meta` fields (`name_snake`, `default`) directly into readable execution examples.
2. **Contextual Introspection**: Employs `exception_context_for_classmethod` to dynamically resolve file, line, and method names from the active runtime frame.
3. **No-Bypass Execution**: Because this function is dedicated solely to the error path, it skips condition evaluations and immediately executes diagnostic assembly and allocation overhead.
"""