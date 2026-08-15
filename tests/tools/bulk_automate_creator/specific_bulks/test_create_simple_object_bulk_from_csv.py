import csv
from .create_simple_object_bulk_from_bulk_dict import create_simple_object_bulk_from_bulk_dict
from .BulkDict import BulkDict
from simplibs.sentinels import UNSET


def _convert_value(v: str):
    if v == "" or v is None:
        return UNSET
    try:
        return int(v)
    except:
        return v

def _convert_type(v: str):
    if v == "" or v is None:
        return UNSET
    return {"int": int, "str": str, "float": float}.get(v, Any)

def _convert_bool(v: str):
    return v.lower() == "true"

def _convert_callable(v: str):
    if not v:
        return UNSET
    raise ValueError("CSV nepodporuje callable — musí být zadáno v JSON/YAML.")


def create_simple_object_bulk_from_csv(csv_string: str):
    reader = csv.DictReader(csv_string.splitlines())

    bulk = []

    for row in reader:
        # Konverze typů
        converted = {
            "class_name": row["class_name"],
            "default": _convert_value(row["default"]),
            "value_type": _convert_type(row["value_type"]),
            "validate": _convert_callable(row["validate"]),
            "logic": _convert_callable(row["logic"]),
            "decompose": _convert_callable(row["decompose"]),
            "return_instance": _convert_bool(row["return_instance"]),
            "as_atom": _convert_bool(row["as_atom"]),
            "mutable": _convert_bool(row["mutable"]),
        }

        bulk.append(BulkDict(**converted))

    return create_simple_object_bulk_from_bulk_dict(tuple(bulk))
