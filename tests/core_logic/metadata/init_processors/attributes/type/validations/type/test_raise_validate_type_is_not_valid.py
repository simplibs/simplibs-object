from typing import Any, NoReturn, TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exceptions_helpers import exception_info_for_type
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike

def raise_validate_type_is_not_valid(
    value_type: Any,
    owner_class: "SimpleClassLike"
) -> NoReturn:
    """
    Validuje, že atribut _type je validním typem.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID TYPE DEFINITION: Value not valid
    ═════════════════════════════════════════════════════════════════
    Expected:  Typ reprezentující výstupní objekt třídy.
    Got:       repr(value) (type)
    Problem:   Třídní atribut '_type' není validní hodotu.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Změňte atribut '_type' tak aby obsahoval validní definici.
         • Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.
         • Atribut '_type' je anotací pro hodnotu kterou reprezentuje třídní default.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _type: type = samostatně definované typy jako je 'str', 'int', atd.
         •     _type: UnionType = union type definice pro více povolených typů.
         •     _type: tuple[type, ...] = tuple obsahujích více povolených typů (bude převedeno na UnionType).
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # Podmínka výjimky
    # if not isinstance(value_type, (type, UnionType, tuple)):

    # 1. Vypočet proměných
    (class_name,
     class_parrent,
     error_name,
     context,
     acceptable_definitions
     ) = exception_info_for_type(owner_class)

    # 2. Vyovlání výjimky
    raise SimpleMetadataError(
        error_name=error_name,
        label="Value not valid",
        value=value_type,
        expected="Typ reprezentující výstupní objekt třídy.",
        problem="Třídní atribut '_type' není validní hodotu.",
        context=context,
        how_to_fix=(
            "Změňte atribut '_type' tak aby obsahoval validní definici.",
            "Třídní typ musí odpovídat hodnotě kterou třída reprezentuje.",
            "Atribut '_type' je anotací pro hodnotu kterou reprezentuje třídní default.",
        ) + acceptable_definitions,
        exception=TypeError
    )