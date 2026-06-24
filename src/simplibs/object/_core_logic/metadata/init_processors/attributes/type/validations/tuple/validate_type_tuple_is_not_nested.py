from typing import Any
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_type


def validate_type_tuple_is_not_nested(
    inner_type: Any,
    type_tuple: tuple[Any, ...],
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že atribut _type definovaný jako tuple, nebobsahuje vnořené tuple.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID TYPE DEFINITION: Nested tuple detected
    ═════════════════════════════════════════════════════════════════
    Expected:  Typ reprezentující výstupní objekt třídy.
    Got:       repr(value) (type)
    Problem:   Třídní atribut '_type' je definován jako tuple obsahující vnitřní tuple.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.
         • Atribut '_type' je anotací pro hodnotu kterou reprezentuje třídní default.
         • Definice více typů skrze tuple nesmí obsahovat vnitřní tuple.
         • Převeďte vnořený tuple na plochou strukturu.
         • Například místo '(int, (str, float))' použijte '(int, str, float)'.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _type: type = samostatně definované typy jako je 'str', 'int', atd.
         •     _type: UnionType = union type definice pro více povolených typů.
         •     _type: tuple[type, ...] = tuple obsahujích více povolených typů (bude převedeno na UnionType).
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if isinstance(inner_type, tuple):

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
            value_label=f"{class_name}._type",
            value=type_tuple,
            expected="Typ reprezentující výstupní objekt třídy.",
            problem=f"Třídní atribut '_type' je definován jako tuple obsahující vnitřní tuple.",
            context=context,
            how_to_fix=(
                "Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.",
                "Atribut '_type' je anotací pro hodnotu kterou reprezentuje třídní default.",
                "Definice více typů skrze tuple nesmí obsahovat vnitřní tuple.",
                "Převeďte vnořený tuple na plochou strukturu.",
                "Například místo '(int, (str, float))' použijte '(int, str, float)'.",
            ) + acceptable_definitions,
            exception=TypeError
        )