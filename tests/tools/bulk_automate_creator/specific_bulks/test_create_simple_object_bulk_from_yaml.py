import yaml
from .create_simple_object_bulk_from_bulk_dict import create_simple_object_bulk_from_bulk_dict
from .BulkDict import BulkDict

def create_simple_object_bulk_from_yaml(yaml_string: str):
    data = yaml.safe_load(yaml_string)

    if not isinstance(data, list):
        raise ValueError("YAML musí být list objektů.")

    bulk = tuple(
        BulkDict(**item)
        for item in data
    )

    return create_simple_object_bulk_from_bulk_dict(bulk)
