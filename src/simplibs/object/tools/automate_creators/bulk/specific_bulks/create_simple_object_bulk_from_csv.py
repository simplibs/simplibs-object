import csv
from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ..BulkCase import BulkCase
# Inners
from .create_simple_object_bulk_from_bulk_case_class import create_simple_object_bulk_from_bulk_case_class
from ._validations import (
    raise_bulk_input_not_str,
    raise_bulk_csv_callable_not_supported,
)


def _convert_value(v: str | None) -> Any:
    if v is None or v.strip() == "":
        return UNSET
    val = v.strip()
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def _convert_type(v: str | None) -> Any:
    if v is None or v.strip() == "":
        return UNSET
    types_map = {"int": int, "str": str, "float": float, "bool": bool}
    return types_map.get(v.strip().lower(), Any)


def _convert_bool(v: str | None) -> bool:
    if v is None:
        return False
    return v.strip().lower() in ("true", "1", "yes")


def _convert_callable(v: str | None, param_name: str) -> Any:
    if not v or v.strip() == "":
        return UNSET
    raise_bulk_csv_callable_not_supported(param_name)


def create_simple_object_bulk_from_csv(csv_string: str):
    """Parses a CSV string with headers and creates a bulk collection of Simple objects."""
    if not isinstance(csv_string, str):
        raise_bulk_input_not_str(csv_string, "csv")

    reader = csv.DictReader(csv_string.strip().splitlines())
    bulk = []

    for row in reader:
        converted = {
            "class_name": row.get("class_name"),
            "default": _convert_value(row.get("default")),
            "value_type": _convert_type(row.get("value_type")),
            "validate": _convert_callable(row.get("validate"), "validate"),
            "logic": _convert_callable(row.get("logic"), "logic"),
            "decompose": _convert_callable(row.get("decompose"), "decompose"),
            "return_instance": _convert_bool(row.get("return_instance")),
            "as_atom": _convert_bool(row.get("as_atom")),
            "mutable": _convert_bool(row.get("mutable")),
        }
        bulk.append(BulkCase(**converted))

    return create_simple_object_bulk_from_bulk_case_class(tuple(bulk))