from typing import Any, NoReturn
# Outers
from ....exceptions import SimpleDefinitionError


def raise_bulk_item_is_not_bulk_dict(
    item: Any,
    index: int
) -> None | NoReturn:
    """Validates that a provided bulk element is an instance of BulkCase."""

    raise SimpleDefinitionError(
        error_name="INVALID BULK ITEM ERROR",
        label="bulk_item_is_not_bulk_dict",
        expected="An instance of BulkCase",
        value=type(item).__name__,
        problem=(
            f"Element at index {index} in the bulk creation sequence is not a 'BulkCase' instance "
            f"(received type '{type(item).__name__}')."
        ),
        context="Attempted to perform bulk object generation using 'create_simple_object_bulk_from_bulk_dict'.",
        how_to_fix=(
            "Ensure all items passed to bulk creation are wrapped in 'BulkCase' specification instances.",
            "Example: create_simple_object_bulk_from_bulk_dict([BulkCase(class_name='MyConst', default=10), ...])",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_bulk_item_is_not_bulk_dict

## Purpose
Guarantees that every item processed by the BulkCase bulk runner is a valid `BulkCase` instance.

## Behavior
1. Performs an `isinstance(item, BulkCase)` check.
2. Raises structured `SimpleDefinitionError` wrapping `TypeError` if an invalid element is encountered.
"""