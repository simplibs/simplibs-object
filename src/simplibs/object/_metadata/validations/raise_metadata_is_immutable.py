from typing import Any, NoReturn
# Outers
from ..._types import SimpleClassType
from ...exceptions import SimpleMetadataError


def raise_metadata_is_immutable(
    attr_name: str,
    current_value: Any,
    new_value: Any,
    owner_class: SimpleClassType
) -> NoReturn:
    """
    Vyvolá výjimku při pokusu o změnu již inicializovaných metadat.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METADATA IMMUTABILITY ERROR: Field already initialized
    ═════════════════════════════════════════════════════════════════
    Expected:  Jednou nastavená data již nejde přepisovat.
    Got:       {repr(value)} ({type(value).__name__})
    Problem:   Hodnota je již nastavena a nelze ji změnit: {repr(current_value)}.
    Context:   Pokus o přepsání '{attr_name}' v metadatech třídy '{class_name}'.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Metadata systému Simple jsou navržena jako 'Write-Once'.
         • Po inicializaci hodnoty jsou imutabilní a nejde je dodatečně měnit.
         • Dodatečný přepis je povolen jen pro neinicializované hodnoty.
         • Pravděpodbně dochází k nevalidní operaci, a chyba bude v záměru či provedení.
         • Pokud potřebujete dynamické chování, využijte k tomu určené cache sloty.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Příprava kontextu
    class_name = owner_class.__name__

    # 2. Vyvolání výjimky
    raise SimpleMetadataError(
        error_name="METADATA IMMUTABILITY ERROR",
        value_label="Field already initialized",
        expected="Jednou nastavená data již nejde přepisovat.",
        value=new_value,
        problem=f"Hodnota je již nastavena a nelze ji změnit: {repr(current_value)}.",
        context=f"Pokus o přepsání '{attr_name}' v metadatech třídy '{class_name}'.",
        how_to_fix=(
            "Metadata systému Simple jsou navržena jako 'Write-Once'.",
            "Po inicializaci hodnoty jsou imutabilní a nejde je dodatečně měnit.",
            "Dodatečný přepis je povolen jen pro neinicializované hodnoty.",
            "Pravděpodbně dochází k nevalidní operaci, a chyba bude v záměru či provedení.",
            "Pokud potřebujete dynamické chování, využijte k tomu určené cache sloty."
        ),
        exception=AttributeError
    )