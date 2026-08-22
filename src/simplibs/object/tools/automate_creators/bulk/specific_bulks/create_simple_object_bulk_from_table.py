from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ..BulkCase import BulkCase
# Inners
from .create_simple_object_bulk_from_bulk_case_class import create_simple_object_bulk_from_bulk_case_class
from ._validations import (
    raise_bulk_input_not_sequence,
    raise_bulk_table_row_not_sequence,
)


def create_simple_object_bulk_from_table(table: list[list[Any]]):
    """Creates a bulk collection of Simple objects from a 2D matrix / table."""
    if not isinstance(table, (list, tuple)):
        raise_bulk_input_not_sequence(
            value=table,
            runner_name="create_simple_object_bulk_from_table",
            expected_items_description="2D table rows (lists/tuples)",
        )

    bulk = []
    for index, row in enumerate(table):
        if not isinstance(row, (list, tuple)):
            raise_bulk_table_row_not_sequence(row, index)

        # Změna výchozí hodnoty z None na UNSET
        def _get(idx: int, default: Any = UNSET) -> Any:
            return row[idx] if len(row) > idx else default

        bulk.append(
            BulkCase(
                class_name=_get(0),
                default=_get(1),
                value_type=_get(2),
                validate=_get(3),
                logic=_get(4),
                decompose=_get(5),
                return_instance=_get(6, False),
            )
        )

    return create_simple_object_bulk_from_bulk_case_class(tuple(bulk))