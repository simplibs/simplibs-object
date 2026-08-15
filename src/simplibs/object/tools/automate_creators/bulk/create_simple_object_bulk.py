# create_simple_object_bulk.py
from typing import Any
from .data_classes.bulk_dict import BulkCase
from .specific_bulks.create_simple_object_bulk_from_csv import create_simple_object_bulk_from_csv
from .specific_bulks.create_simple_object_bulk_from_dicts import create_simple_object_bulk_from_dicts
from .specific_bulks.create_simple_object_bulk_from_json import create_simple_object_bulk_from_json
from .specific_bulks.create_simple_object_bulk_from_table import create_simple_object_bulk_from_table
from .specific_bulks.create_simple_object_bulk_from_yaml import create_simple_object_bulk_from_yaml


def create_simple_object_bulk(source: Any):
    """
    Univerzální orchestrátor pro tvorbu bulk objektů.
    Automaticky rozpozná typ vstupu a deleguje zpracování správnému parseru.

    Podporované typy vstupu:
      - list/tuple s instance `BulkCase`
      - list/tuple s Python `dict`
      - 2D list/tuple (`table`)
      - str obsahující JSON
      - str obsahující YAML (pokud začíná nebo obsahuje typické klíče)
      - str obsahující CSV (s hlavičkou class_name)
    """
    # 1. Je to sekvence (List / Tuple)
    if isinstance(source, (list, tuple)):
        if not source:
            return create_simple_object_bulk_from_dicts([])

        first_item = source[0]

        # A) List instancí BulkCase
        if isinstance(first_item, BulkCase):
            from .create_simple_object_bulk_from_bulk_calse_class import (
                create_simple_object_bulk_from_bulk_calse_class,
            )
            return create_simple_object_bulk_from_bulk_calse_class(tuple(source))

        # B) List slovníků
        if isinstance(first_item, dict):
            return create_simple_object_bulk_from_dicts(source)

        # C) Matice / Tabulka (2D list)
        if isinstance(first_item, (list, tuple)):
            return create_simple_object_bulk_from_table(source)

        raise TypeError(f"Nerozpoznatelný prvek v seznamu: {type(first_item)}")

    # 2. Je to Textový řetězec (JSON / YAML / CSV)
    if isinstance(source, str):
        cleaned = source.strip()

        # A) Detekce JSON (začíná '[')
        if cleaned.startswith("["):
            return create_simple_object_bulk_from_json(cleaned)

        # B) Detekce CSV (podle hlavičky 'class_name')
        if "class_name" in cleaned.splitlines()[0]:
            return create_simple_object_bulk_from_csv(cleaned)

        # C) Záložní pokus o YAML
        return create_simple_object_bulk_from_yaml(cleaned)

    raise TypeError(f"Nepodporovaný typ vstupu pro bulk tvorbu: {type(source)}")


"""
# Všechna tato volání vrátí stejný výsledek:

# 1. Univerzální fasáda (Doporučeno)
bulk_1 = create_simple_object_bulk([{"class_name": "MyConstant", "default": 100}])
bulk_2 = create_simple_object_bulk('[{"class_name": "MyConstant", "default": 100}]')
bulk_3 = create_simple_object_bulk([["MyConstant", 100]])

# 2. Explicitní parser (Když uživatel chce 100% jistotu bez auto-detekce)
bulk_4 = create_simple_object_bulk_from_json('[{"class_name": "MyConstant", "default": 100}]')
"""