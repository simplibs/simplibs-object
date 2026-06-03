from typing import Any
# Outers
from .......exceptions import SimpleObjectMetadataError
from ......._types import SimpleClassType
from ..utils import exception_info_for_default


def validate_default_validations_return_true(
    default_value: Any,
    method_validation_outcome: bool,
    expected_type: type,
    calculate_default: Any,
    owner_class: SimpleClassType,
) -> None:
    """
    Validuje, že hodnota '_default' odpovídá definovanému typu '_type'.

    Využívá funkci isinstance, která si díky předchozím validacím poradí
    s atomickými typy, Uniony i plochými tuply.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID DEFAULT DEFINITION: Hodnota neprošla validací
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota typu: {expected_type}.
    Got:       repr(value) (type)
    Problem:   Hodnota odpovídá typově, ale neprošla dodatečnou validační metodou.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Změňte hodnotu '_default' tak, aby odpovídala logice v '_validate'.
         • Nebo upravte logiku '_validate' tak, aby hodnota prošla.
         • Případě můžete i '_default' nedefinovat a pak bude použita defaultní hodnota vypočítaná z inners.
         • Defaultní hodnota vypočítaná z inners je '{calculate_default}'.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not method_validation_outcome:

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         ) = exception_info_for_default(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleObjectMetadataError(
            error_name=error_name,
            value_label="Hodnota neprošla validací",
            expected=f"Hodnota typu: {expected_type}",
            value=default_value,
            problem="Hodnota odpovídá typově, ale neprošla dodatečnou validační metodou.",
            context=context,
            how_to_fix=(
                "Změňte hodnotu '_default' tak, aby odpovídala logice v '_validate'.",
                "Nebo upravte logiku '_validate' tak, aby hodnota prošla.",
                "Případě můžete i '_default' nedefinovat a pak bude použita defaultní hodnota vypočítaná z inners.",
                f"Defaultní hodnota vypočítaná z inners je '{calculate_default}'."
            ),
            exception=ValueError
        )
