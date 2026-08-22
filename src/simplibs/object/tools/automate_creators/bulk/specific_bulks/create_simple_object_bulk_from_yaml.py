# Inners
from .create_simple_object_bulk_from_dicts import create_simple_object_bulk_from_dicts
from ._validations import (
    raise_bulk_input_not_str,
    raise_bulk_yaml_import_failed,
    raise_bulk_decode_failed,
    raise_bulk_data_not_list,
)


def create_simple_object_bulk_from_yaml(yaml_string: str):
    """Parses a YAML string and creates a bulk collection of Simple objects."""
    if not isinstance(yaml_string, str):
        raise_bulk_input_not_str(yaml_string, "yaml")

    try:
        import yaml
    except ImportError:
        raise_bulk_yaml_import_failed()

    try:
        data = yaml.safe_load(yaml_string)
    except Exception as exc:
        raise_bulk_decode_failed(yaml_string, "yaml", exc)

    if not isinstance(data, list):
        raise_bulk_data_not_list(data, "yaml")

    return create_simple_object_bulk_from_dicts(data)