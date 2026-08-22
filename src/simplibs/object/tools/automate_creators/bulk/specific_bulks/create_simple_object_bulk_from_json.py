import json
# Inners
from .create_simple_object_bulk_from_dicts import create_simple_object_bulk_from_dicts
from ._validations import (
    raise_bulk_input_not_str,
    raise_bulk_decode_failed,
    raise_bulk_data_not_list,
)


def create_simple_object_bulk_from_json(json_string: str):
    """Parses a JSON string and creates a bulk collection of Simple objects."""
    if not isinstance(json_string, str):
        raise_bulk_input_not_str(json_string, "json")

    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as exc:
        raise_bulk_decode_failed(json_string, "json", exc)

    if not isinstance(data, list):
        raise_bulk_data_not_list(data, "json")

    return create_simple_object_bulk_from_dicts(data)