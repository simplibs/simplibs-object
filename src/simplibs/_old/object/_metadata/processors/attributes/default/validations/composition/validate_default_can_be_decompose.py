from typing import Any, Callable
# Outers
from .......exceptions import SimpleObjectMetadataError
from ......._types import SimpleClassType
from ..utils import exception_info_for_default


def validate_default_can_be_decompose(
    default_value: Any,
    decompose_method: Callable,
    calculate_default: Any,
    owner_class: SimpleClassType,
) -> None:
    """
    Validuje, že hodnota '_default' odpovídá definovanému typu '_type'.

    Využívá funkci isinstance, která si díky předchozím validacím poradí
    s atomickými typy, Uniony i plochými tuply.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID DEFAULT DEFINITION: Hodnotu není možné rozložit
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota, rozložitelná pomocí metody '_decompose'.
    Got:       repr(value) (type)
    Problem:   Metoda pro rozklad vrátila výjimku.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Při pokusu o rozložení hodnoty metodou '_decompose' došlo k vyvolání výjimky.
         • Zkontrolujte hodnotu a nebo metodu pro rozklad.
         • Metoda pro rozklad už byla validavoaná na vypočítaný default na základě hodnot z '_inners'.
         • (Chyba tedy bude spíše v definici defaultní hodnoty.)
         • Případně můžete '_default' nevyplňovat a míto něj bude použit vypočtený: {calculate_default}.
         • Bližší informace vyvolané výjimky jsou uvedené níže v sekci 'Intercepted exception'.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Zkušební výpočet
    try:
        decompose_method(default_value)
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
            value_label="Hodnotu není možné rozložit",
            expected=f"Hodnota, rozložitelná pomocí metody '_decompose'.",
            value=default_value,
            problem="Metoda pro rozklad vrátila výjimku.",
            context=context,
            how_to_fix=(
                "Při pokusu o rozložení hodnoty metodou '_decompose' došlo k vyvolání výjimky.",
                "Zkontrolujte hodnotu a nebo metodu pro rozklad.",
                "Metoda pro rozklad už byla validavoaná na vypočítaný default na základě hodnot z '_inners'.",
                "(Chyba tedy bude spíše v definici defaultní hodnoty.)",
                f"Případně můžete '_default' nevyplňovat a míto něj bude použit vypočtený: {calculate_default}.",
                "Bližší informace vyvolané výjimky jsou uvedené níže v sekci 'Intercepted exception'.",
            ),
            exception=e
        )