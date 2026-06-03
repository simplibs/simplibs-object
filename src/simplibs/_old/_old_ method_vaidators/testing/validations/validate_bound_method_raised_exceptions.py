# Outers
from .....exceptions import SimpleObjectMetadataError
from ...utils import exception_context_for_classmethod


def validate_bound_method_raised_exceptions(
    intercepted_exception: Exception,
    bound_method: classmethod,
) -> None:
    """
    Validuje, že zkušební výpočet metody proběhl bez vyvolání výjimky.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Zkušební výpočet vyvolal výjimku
    ═════════════════════════════════════════════════════════════════
    Expected:  Úspěšné dokončení výpočtu bez vyvolání výjimky..
    Problem:   Během zkušebního výpočtu nastala chyba.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Zkontrolujte vnitřní logiku metody '{method_name}'.
         • Prověřte, zda metoda korektně zpracovává své defaultní hodnoty.
         • Detailní příčina selhání je uvedena níže v 'Intercepted exception'.
    ═════════════════════════════════════════════════════════════════
    Intercepted exception ({ExceptionType}):
        {ErrorMessage}
    """

    # 1. Podmínka výjimky
    if intercepted_exception:

        # 2. Výpočet proměnných
        class_name, method_name, context = exception_context_for_classmethod(bound_method)

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD LOGIC ERROR",
            value_label="Výjimka při zkušebním výpočtu",
            expected="Úspěšné dokončení výpočtu bez vyvolání výjimky.",
            problem="Během zkušebního výpočtu nastala chyba.",
            context=context,
            how_to_fix=(
                f"Zkontrolujte vnitřní logiku metody '{method_name}'.",
                "Prověřte, zda metoda korektně zpracovává své defaultní hodnoty.",
                "Detailní příčina selhání je uvedena níže v 'Intercepted exception."
            ),
            exception=intercepted_exception
        )