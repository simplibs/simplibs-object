import inspect
from typing import Any
from simplibs.signature import create_keyword_parameter
# Outers
from ...._types import SimpleMetaType, SimpleClassType


def make_atom_param(
    owner_class: SimpleClassType
) -> inspect.Parameter:
    """
    Doménová továrna pro vytvoření signatury atomického parametru.
    Vytahuje data z metadat třídy a balí je do formátu inspect.Parameter.
    """

    # 1. Získání metadat
    # Předpokládáme, že owner_class už prošla procesem inicializace metadat
    meta: SimpleMetaType = owner_class.meta

    # 2. Výroba parametru
    # Používáme tvou utilitu create_keyword_parameter.
    # Data bereme z již zprocesovaných a validovaných polí v metadatech.
    return create_keyword_parameter(
        name=meta.name_snake,
        default=meta.default,
        annotation=meta.value_type,
        validate=False  # Validaci vypínáme, protože metadata jsou již "posvěcená"
    )