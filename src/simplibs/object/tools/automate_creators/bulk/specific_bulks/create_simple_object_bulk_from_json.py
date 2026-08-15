# create_simple_object_bulk_from_json.py
import json
from .create_simple_object_bulk_from_dicts import create_simple_object_bulk_from_dicts


def create_simple_object_bulk_from_json(json_string: str):
    """Parse JSON řetězce a vytvoří bulk."""
    if not isinstance(json_string, str):
        raise TypeError("Vstupní JSON musí být string.")

    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Neplatný JSON formát: {e}") from e

    if not isinstance(data, list):
        raise ValueError("JSON musí obsahovat list objektů (slovníků).")

    return create_simple_object_bulk_from_dicts(data)
