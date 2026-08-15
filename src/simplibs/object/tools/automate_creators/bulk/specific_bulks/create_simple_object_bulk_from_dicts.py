# create_simple_object_bulk_from_dicts.py
from typing import Any
from ...data_classes.bulk_dict import BulkCase
from ..create_simple_object_bulk_from_bulk_calse_class import create_simple_object_bulk_from_bulk_calse_class


def create_simple_object_bulk_from_dicts(dicts: list[dict[str, Any]]):
    """Vytvoří bulk z kolekce slovníků."""
    if not isinstance(dicts, (list, tuple)):
        raise TypeError("Vstup musí být list nebo tuple slovníků.")

    bulk = tuple(BulkCase(**d) for d in dicts)
    return create_simple_object_bulk_from_bulk_calse_class(bulk)