from typing import Any
from simplibs.sentinels import UNSET
# Outers
from .......exceptions import SimpleObjectMetadataError
from ......._types import SimpleClassType
from ..utils import exception_info_for_type


def validate_type_is_defined(
    atrribut_value: Any,
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že atribut _type je na třídě definovaný.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID TYPE DEFINITION: Attribut '_type' není definovaný
    ═════════════════════════════════════════════════════════════════
    Expected:  Třída musí deklarovat svůj datový typ pro zajištění integrity.
    Problem:   Třída atribut '_type' vůbec nedefinuje.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Definujte atribut '_type' ve třídě '{class_name}'.
         . Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _type: type = samostatně definované typy jako je 'str', 'int', atd.
         •     _type: UnionType = union type definice pro více povolených typů.
         •     _type: tuple[type, ...] = tuple obsahujích více povolených typů (bude převedeno na UnionType).
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if atrribut_value is UNSET:

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_type(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleObjectMetadataError(
            error_name=error_name,
            value_label="Attribut '_type' není definovaný",
            expected="Třída musí deklarovat svůj datový typ pro zajištění integrity.",
            problem=f"Třída atribut '_type' vůbec nedefinuje.",
            context=context,
            how_to_fix=(
                f"Definujte atribut '_type' ve třídě '{class_name}'.",
                "Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.",
            ) + acceptable_definitions,
            exception=AttributeError
        )