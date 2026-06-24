from typing import Any
from simplibs.sentinels import UNSET
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_inners


def validate_inners_is_defined(
    atrribut_value: Any,
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že atribut _inners je na třídě definovaný.

    Tato validace by nikdy neměla nastat protože k ověření,
    že třída obsahuje atribut '_inners' dochází v kodu již dříve,
    při rozhodnutí, zda se jedná o třídu kompoziční a nebo s konstantou.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Attribut není definovaný
    ═════════════════════════════════════════════════════════════════
    Expected:  Attribut '_inners' obsahující vnitřní prvky kompozice.
    Problem:   Attribut není na třídě nedefinovaný.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Třída kompozice (SimpleObject) musí deklarovat attribut '_inners'.
         • Definujte atribut '_inners' ve třídě '{class_name}'.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _inners: tuple = (PrvekA, PrvekB)
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if atrribut_value is UNSET:

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label="Attribut '_inners' není definovaný",
            expected=f"Attribut '_inners' obsahující vnitřní prvky kompozice.",
            problem=f"Attribut není na třídě nedefinovaný.",
            context=context,
            how_to_fix=(
                "Třída kompozice (SimpleObject) musí deklarovat attribut '_inners'.",
                f"Definujte atribut '_inners' ve třídě '{class_name}'.",
            ) + acceptable_definitions,
            exception=AttributeError
        )