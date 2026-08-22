from typing import Any, NoReturn
from ......exceptions import SimpleRuntimeError


def raise_bulk_table_row_not_sequence(
    row: Any,
    index: int,
) -> None | NoReturn:
    """Raises SimpleRuntimeError when a specific row in 2D matrix input is not a sequence."""

    raise SimpleRuntimeError(
        error_name="INVALID BULK TABLE ROW ERROR",
        label="bulk_table_row_is_not_sequence",
        expected="A list or tuple representing a 2D table row",
        value=type(row).__name__,
        problem=(
            f"Row at index {index} in the 2D bulk table input is not a sequence "
            f"(received type '{type(row).__name__}')."
        ),
        context="Attempted bulk creation using 'create_simple_object_bulk_from_table'.",
        how_to_fix=(
            f"Ensure every row inside the 2D matrix is wrapped in a list or tuple.",
            f"Example format: [[class_name, default, ...], [class_name_2, default_2, ...]]",
        ),
        exception=TypeError,
    )