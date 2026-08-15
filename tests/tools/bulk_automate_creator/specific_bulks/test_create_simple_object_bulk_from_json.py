import json
from typing import Any
from .create_simple_object_bulk_from_bulk_dict import create_simple_object_bulk_from_bulk_dict
from .BulkDict import BulkDict


def create_simple_object_bulk_from_json(json_string: str):
    data = json.loads(json_string)

    if not isinstance(data, list):
        raise ValueError("JSON musí být list objektů.")

    bulk = tuple(
        BulkDict(**item)
        for item in data
    )

    return create_simple_object_bulk_from_bulk_dict(bulk)
