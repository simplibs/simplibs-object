# create_simple_object_bulk_from_yaml.py
from .create_simple_object_bulk_from_dicts import create_simple_object_bulk_from_dicts


def create_simple_object_bulk_from_yaml(yaml_string: str):
    """Parse YAML řetězce a vytvoří bulk."""
    if not isinstance(yaml_string, str):
        raise TypeError("Vstupní YAML musí být string.")

    try:
        import yaml
    except ImportError:
        raise ImportError(
            "Pro načítání YAML je potřeba nainstalovat balíček PyYAML: `pip install pyyaml`"
        )

    try:
        data = yaml.safe_load(yaml_string)
    except Exception as e:
        raise ValueError(f"Neplatný YAML formát: {e}") from e

    if not isinstance(data, list):
        raise ValueError("YAML musí obsahovat list objektů (slovníků).")

    return create_simple_object_bulk_from_dicts(data)