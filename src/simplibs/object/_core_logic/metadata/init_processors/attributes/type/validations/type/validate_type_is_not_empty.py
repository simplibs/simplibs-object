from typing import Any
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_type


def validate_type_is_not_empty(
    processed_type: Any,
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že atribut _type nemá prázdnou hodnotu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID TYPE DEFINITION: Empty definition is not allowed
    ═════════════════════════════════════════════════════════════════
    Expected:  Typ reprezentující výstupní objekt třídy.
    got:       '()' (tuple)
    Problem:   Třídní atribut '_type' nesmí být prázdným objektem.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         . Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.
         • Definice typu nesmí být prázdná, aby bylo možné provádět validace hodnot..
         • Změňte atribut '_type' tak aby odpovídal objektu který třída reprezentuje..
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _type: type = samostatně definované typy jako je 'str', 'int', atd.
         •     _type: UnionType = union type definice pro více povolených typů.
         •     _type: tuple[type, ...] = tuple obsahujích více povolených typů (bude převedeno na UnionType).
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not processed_type:

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_type(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label=f"Empty definition is not allowed",
            value=processed_type,
            expected="Typ reprezentující výstupní objekt třídy.",
            problem="Třídní atribut '_type' nesmí být prázdným objektem.",
            context=context,
            how_to_fix=(
                "Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.",
                "Definice typu nesmí být prázdná, aby bylo možné provádět validace hodnot.",
                "Změňte atribut '_type' tak aby odpovídal objektu který třída reprezentuje.",
            ) + acceptable_definitions,
            exception=ValueError
        )