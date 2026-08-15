from typing import Any

from .create_simple_object_bulk_from_bulk_dict import create_simple_object_bulk_from_bulk_dict
from .BulkDict import BulkDict


def create_simple_object_bulk_from_dicts(dicts: list[dict[str, Any]]):
    bulk = tuple(
        BulkDict(**d)
        for d in dicts
    )

    return create_simple_object_bulk_from_bulk_dict(bulk)
