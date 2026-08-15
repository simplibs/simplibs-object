import csv
from typing import Any
from ...data_classes.bulk_dict import BulkCase
from ...data_classes.unset import UNSET
from ..create_simple_object_bulk_from_bulk_calse_class import create_simple_object_bulk_from_bulk_calse_class


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


def _convert_callable(v: str | None) -> Any:
    if not v or v.strip() == "":
        return UNSET
    raise ValueError(
        "CSV nepodporuje callable objekty (logic/validate/decompose). "
        "Použijte JSON/YAML nebo přímé Python slovníky."
    )


def create_simple_object_bulk_from_csv(csv_string: str):
    """Parse CSV řetězce s hlavičkou a vytvoří bulk."""
    if not isinstance(csv_string, str):
        raise TypeError("Vstupní CSV musí být string.")

    reader = csv.DictReader(csv_string.strip().splitlines())
    bulk = []

    for row in reader:
        converted = {
            "class_name": row.get("class_name"),
            "default": _convert_value(row.get("default")),
            "value_type": _convert_type(row.get("value_type")),
            "validate": _convert_callable(row.get("validate")),
            "logic": _convert_callable(row.get("logic")),
            "decompose": _convert_callable(row.get("decompose")),
            "return_instance": _convert_bool(row.get("return_instance")),
            "as_atom": _convert_bool(row.get("as_atom")),
            "mutable": _convert_bool(row.get("mutable")),
        }
        bulk.append(BulkCase(**converted))

    return create_simple_object_bulk_from_bulk_calse_class(tuple(bulk))