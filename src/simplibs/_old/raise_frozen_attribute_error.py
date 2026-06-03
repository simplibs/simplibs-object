from typing import Any, NoReturn
# Outers
from ..._types import SimpleClassType
from ...exceptions import SimpleObjectMetadataError

def raise_frozen_attribute_error(
    cls: SimpleClassType,
    attr_name: str,
    new_value: Any
) -> NoReturn:
    """
    Vyvolá výjimku při pokusu o změnu zmrazeného definičního atributu třídy.

    ═════════════════════════════════════════════════════════════════
    ⚠️ CLASS DEFINITION ERROR: Pokus o změnu základního prvku
    ═════════════════════════════════════════════════════════════════
    Expected:  Prvek je uzamčený pro změnu a určen pouze ke čtení.
    Got:       {repr(value)} ({type(value).__name__})
    Problem:   Hodnota je již nastavena a nelze ji změnit.
    Context:   Pokus o přepsání '{attr_name}' v třídě '{class_name}'.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Definiční prvky třídy nelze měnit za běhu programu.
         • Definiční prvky jsou: _default, _type, _inners, _logic, _decompose, _validate.
         • Pokud je chcete změnit, musíte tak učinit přímo v deklaraci třídy '{class_name}'.
         • Tato ochrana zajišťuje, že základní struktura třídy zůstane konstantní.
         • Zkontrolujte, proces vyvolající pokus o tento přepis.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Příprava kontextu
    class_name = cls.__name__

    # 2. Vyvolání výjimky
    raise SimpleObjectMetadataError(
        error_name="CLASS DEFINITION FROZEN",
        value_label="Pokus o změnu základního prvku",
        expected="Prvek je uzamčený pro změnu a určen pouze ke čtení..",
        value=new_value,
        problem="Hodnota je již nastavena a nelze ji změnit.",
        context=f"Pokus o přepsání '{attr_name}' v třídě '{class_name}'.",
        how_to_fix=(
            "Definiční prvky třídy nelze měnit za běhu programu.",
            "Definiční prvky jsou: _default, _type, _inners, _logic, _decompose, _validate.",
            "Tato ochrana brání desynchronizaci metadat a logiky objektu.",
            f"Pokud je chcete změnit, musíte tak učinit přímo v deklaraci třídy '{class_name}'.",
            "Tato ochrana zajišťuje, že základní struktura třídy zůstane konstantní.",
            "Zkontrolujte, zda se nepokoušíte o nevalidní monkey-patching."
            "Zkontrolujte, proces vyvolající pokus o tento přepis."
        ),
        exception=AttributeError
    )