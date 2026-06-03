# Outers
from ......._types import SimpleMetaType


def build_init_signature_string(meta: SimpleMetaType) -> str:
    """
    Sestaví pouze čistá jména parametrů pro __init__ bez anotací a defaultů.
    Všechny parametry jsou striktně Keyword-Only (*).

    Výsledek: "self, *, cena, barva, vykon"
    """
    param_pieces = ["self", "*"]

    # Stačí nám jen projít klíče (jména parametrů)
    for name_snake in meta.constants_map.keys():
        param_pieces.append(name_snake)

    return ", ".join(param_pieces)