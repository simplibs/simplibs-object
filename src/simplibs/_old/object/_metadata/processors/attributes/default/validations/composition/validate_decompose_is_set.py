from typing import Any, Callable
# Outers
from .......exceptions import SimpleObjectMetadataError
from ......._types import SimpleClassType
from ..utils import exception_info_for_default


def validate_decompose_is_set(
    decompose_method: Callable,
    calculate_default: Any,
    owner_class: SimpleClassType,
) -> None:
    """
    Validuje, že hodnota '_default' odpovídá definovanému typu '_type'.

    Využívá funkci isinstance, která si díky předchozím validacím poradí
    s atomickými typy, Uniony i plochými tuply.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID DEFAULT DEFINITION: Chybí pomocná metoda pro rozklad
    ═════════════════════════════════════════════════════════════════
    Expected:  Metoda '_decompose' pro rozklad předané defualtní hodoty.
    Problem:   Definovaný default není možné použít, chybý metoda '_decompose'.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Pro použití defaultní hodnoty je potřeba mít definovanou metodu pro její rozklad '_decompose'.
         • Metda '_decompose' není momentálně definovaná.
         • Buď dodefinujde metodu '_decompose' pro rozklad.
         • Nebo nezadávejte '_default' a k změně defaultní hodnoty použijte defaultních hodnot v metodě '_logic'.
         • (Když v metodě '_logic' zapíšete defaultní hodnoty, přetížíte ty z '_inners'.).
         • Případně můžete '_default' nevyplňovat a míto něj bude použit vypočtený: {calculate_default}.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not decompose_method or not callable(decompose_method):

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         ) = exception_info_for_default(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleObjectMetadataError(
            error_name=error_name,
            value_label="Chybí pomocná metoda pro rozklad",
            expected=f"Metoda '_decompose' pro rozklad předané defualtní hodoty.",
            problem="Definovaný default není možné použít, chybý metoda '_decompose'.",
            context=context,
            how_to_fix=(
                "Pro použití defaultní hodnoty je potřeba mít definovanou metodu pro její rozklad '_decompose'.",
                "Metda '_decompose' není momentálně definovaná a nebo není volatelný objekt.",
                "Buď dodefinujde metodu '_decompose' pro rozklad.",
                "Nebo nezadávejte '_default' a k změně defaultní hodnoty použijte defaultních hodnot v metodě '_logic'.",
                "(Když v metodě '_logic' zapíšete defaultní hodnoty, přetížíte ty z '_inners'.)",
                f"Případně můžete '_default' nevyplňovat a míto něj bude použit vypočtený: {calculate_default}.",
            ),
            exception=AttributeError
        )