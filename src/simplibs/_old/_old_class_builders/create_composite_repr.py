from typing import Callable
# Outers
from ....._types import SimpleMetaType


def create_repr(
    meta: SimpleMetaType
) -> Callable:
    """
    Vytváří textovou reprezentaci kompozitní instance.
    Ukazuje jméno hlavní třídy a vypisuje hodnoty všech jejích vnitřních konstant.

    Výsledek může vypadat takto: Auto(vykon=150, barva='červená')
    """

    # 1. Definice metody
    def __repr__(self):

        # 1.1 Vytvoření řetězce pro parametry
        params_str = ", ".join([
            f"{name_snake}={getattr(self, const_meta.name_private).value!r}"
            for name_snake, const_meta in meta.constants_map.items()
        ])

        # 1.2 Navrácení řetězce s jménem tířdy a parametry
        return f"{meta.class_name}({params_str})"

    # 2. Navrácení metody
    return __repr__
