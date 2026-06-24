from typing import NoReturn
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_type


def raise_union_type_contain_none(
    owner_class: SimpleClassType
) -> NoReturn:
    """
    Validuje, že atribut _type neobsahuje hodnotu None.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID TYPE DEFINITION: Value 'None' detected
    ═════════════════════════════════════════════════════════════════
    Expected:  Typ reprezentující výstupní objekt třídy.
    Problem:   Třídní atribut '_type' obsahuje hodnotu 'None'.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Změňte atribut '_type' tak aby neobsahoval hodnotu 'None'.
         • Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.
         • Atribut '_type' je anotací pro hodnotu kterou reprezentuje třídní default.
         • Hodnota kterou třída reprezentuje, nesmí být 'None'.
         • To znamená, že typ, který reprezentuje tuto třídní hodnotu nesmí být 'None'.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _type: type = samostatně definované typy jako je 'str', 'int', atd.
         •     _type: UnionType = union type definice pro více povolených typů.
         •     _type: tuple[type, ...] = tuple obsahujích více povolených typů (bude převedeno na UnionType).
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # Podmínka výjimky
    # if isinstance(processed_type, UnionType) and NoneType in processed_type.__args__:

    # 1. Vypočet proměných
    (class_name,
     class_parrent,
     error_name,
     context,
     acceptable_definitions
     ) = exception_info_for_type(owner_class)

    # 2. Vyvolání výjimky
    raise SimpleMetadataError(
        error_name=error_name,
        value_label="Value 'None' detected",
        expected="Typ reprezentující výstupní objekt třídy.",
        problem="Třídní atribut '_type' obsahuje hodnotu 'None'",
        context=context,
        how_to_fix=(
            "Změňte atribut '_type' tak aby neobsahoval hodnotu 'None'",
            "Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.",
            "Atribut '_type' je anotací pro hodnotu kterou reprezentuje třídní default.",
            "Hodnota kterou třída reprezentuje, nesmí být 'None'.",
            "To znamená, že typ, který reprezentuje tuto třídní hodnotu nesmí být 'None'."
        ) + acceptable_definitions,
        exception=TypeError
    )