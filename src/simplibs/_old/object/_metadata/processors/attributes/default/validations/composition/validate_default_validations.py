from typing import Any, Callable
# Outers
from .......exceptions import SimpleObjectMetadataError
from ......._types import SimpleClassType
from ..utils import exception_info_for_default


def validate_default_validations(
    default_value: Any,
    expected_type: Any,
    vlidate_method: Callable,
    calculate_default: Any,
    owner_class: SimpleClassType,
) -> None:
    """
    Validuje, že hodnota '_default' odpovídá definovanému typu '_type'.

    Využívá funkci isinstance, která si díky předchozím validacím poradí
    s atomickými typy, Uniony i plochými tuply.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID DEFAULT DEFINITION: Hodnota neprošla validační metodou
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota typu: {expected_type}.
    Got:       repr(value) (type)
    Problem:   Definovaný default odpovídá typu, ale neprošel validační metodou.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Definovaná validační metoda vrátila výjimku.
         • Tato chyba může nastat protože předaný default neodpovídá validační logice.
         • Případě můžete být způsobena chybnou validační logikou definovanou jako _validate.
         • Metoda _validate již byla ověřena na vypočtený default který jejím ověřením prošel.
         • Defaultní hodnota vypočítaná z inners je '{calculate_default}'.
         • Bližší informace vyvolané výjimky jsou uvedené níže v sekci 'Intercepted exception'.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Zkušební výpočet
    try:
        vlidate_method(default_value)
    except Exception as e:

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         ) = exception_info_for_default(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleObjectMetadataError(
            error_name=error_name,
            value_label="Hodnota neprošla validační metodou",
            expected=f"Hodnota typu: {expected_type}",
            value=default_value,
            problem="Definovaný default odpovídá typu, ale neprošel validační metodou.",
            context=context,
            how_to_fix=(
                "Definovaná validační metoda vrátila výjimku."
                "Tato chyba může nastat protože předaný default neodpovídá validační logice."
                "Případě můžete být způsobena chybnou validační logikou definovanou jako _validate."
                "Metoda _validate již byla ověřena na vypočtený default který jejím ověřením prošel."
                f"Defaultní hodnota vypočítaná z inners je '{calculate_default}'."
                "Bližší informace vyvolané výjimky jsou uvedené níže v sekci 'Intercepted exception'."
            ),
            exception=e
        )