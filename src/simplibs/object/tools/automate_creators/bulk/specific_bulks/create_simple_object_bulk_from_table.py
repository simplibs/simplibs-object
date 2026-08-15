# create_simple_object_bulk_from_table.py
from typing import Any
from ...data_classes.bulk_dict import BulkCase
from ..create_simple_object_bulk_from_bulk_calse_class import create_simple_object_bulk_from_bulk_calse_class


def create_simple_object_bulk_from_table(table: list[list[Any]]):
    """
    Vytvoří bulk z matice / 2D tabulky.
    Podporuje neúplné řádky s využitím bezpečného načítání sloupce.
    """
    if not isinstance(table, (list, tuple)):
        raise TypeError("Vstup musí být 2D list nebo tuple.")

    bulk = []
    for row in table:
        if not isinstance(row, (list, tuple)):
            raise TypeError("Každý řádek tabulky musí být list nebo tuple.")

        # Bezpečný odchyt hodnot podle indexu
        def _get(idx: int, default: Any = None) -> Any:
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

    return create_simple_object_bulk_from_bulk_calse_class(tuple(bulk))