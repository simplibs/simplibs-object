from typing import Callable
# Outers
from ....._types import SimpleMetaType
from ....constants import INDENT
# Inners
from .recalculate_up_helpers.recalculate_up_exec_code import recalculate_up_exec_code


def create_recalculate_up(
    meta: SimpleMetaType
) -> Callable:
    """
    Zkompiluje _recalculate_up do podoby spustitelné funkce.
    """

    # 1. Získání kodu metody
    _recalculate_up = recalculate_up_exec_code(meta)

    # 2. Definice jména metody
    _recalculate_up.__name__ = "_recalculate_up"

    # 3. Definice qualname
    _recalculate_up.__qualname__ = f"{meta.class_name}._recalculate_up"

    # 4. Definice docstringu metody
    _recalculate_up.__doc__ = (
        f"Přepočítá hodnotu kompozice {meta.class_name} směrem nahoru v hierarchii.\n"
        f"\n"
        f"Tato metoda provádí reaktivní aktualizaci stavu. Spustí se automaticky, jakmile\n"
        f"dojde ke změně hodnoty některého z vnitřních prvků (atomů či sub-kompozic).\n"
        f"Pokud nově vypočítaná hodnota neodpovídá původní, uloží se do vnitřního slotu\n"
        f"a změna se propaguje nadřazenému vlastníkovi (ownerovi), pokud existuje.\n"
        f"\n"
        f"Returns:\n"
        f"{INDENT}None"
    )

    # 5. Definice anotací (návratové hodnoty)
    _recalculate_up.__annotations__ = {"return": None}

    # 6. Navrácení zpracované metody
    return _recalculate_up