from typing import NoReturn
# Outers
from .exceptions import SimpleObjectLogicError

def raise_abstract_instantiation_error(
    instance: object
) -> NoReturn:
    """
    Vyvolá výjimku při pokusu o instanciaci abstraktní základní třídy.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INSTANTIATION ERROR: Nepřípustná inicializace třídy
    ═════════════════════════════════════════════════════════════════
    Expected:  Použití třídy jako statického předpisu (deklarace).
    Problem:   Tato třída slouží pouze jako báze a nelze ji instanciovat.
    Context:   Pokus o vytvoření instance třídy '{class_name}'.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Třídy jako SimpleBase, SimpleConstant a SimpleObject jsou abstraktní.
         • Slouží k definici struktury a metadat, nikoliv k držení dat.
         • Pro práci s hodnotami použijte metody pro generování jader:
         •   - .make_core() pro vytvoření hodnotového jádra (Atom).
         •   - .make_atomic_instance() pro vytvoření funkční instance.
         • Tyto metody vygenerují novou třídu, která je již instancovatelná.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Příprava dat
    class_name = instance.__class__.__name__

    # # 2. Vyvolání výjimky
    # raise SimpleObjectLogicError(
    #     error_name="INSTANTIATION ERROR",
    #     value_label="Nepřípustná inicializace třídy",
    #     expected="Použití třídy jako statického předpisu (deklarace).",
    #     problem=f"Třídu '{class_name}' není možné přímo instanciovat.",
    #     context=f"Pokus o vytvoření instance třídy '{class_name}'.",
    #     how_to_fix=(
    #         f"Třídy jako SimpleBase, SimpleConstant a SimpleObject jsou abstraktní.",
    #         "Slouží k definici struktury a metadat, nikoliv k držení dat.",
    #         "Pro práci s hodnotami použijte metody pro generování instančních tříd:",
    #         "  - .make_core() pro vytvoření hodnotového jádra (Atom).",
    #         "  - .make_atomic_instance() pro vytvoření funkční instance.",
    #         "Tyto metody vygenerují novou třídu, která je již připravena pro instanciaci."
    #     ),
    #     exception=TypeError
    # )

    raise SimpleObjectLogicError(
        error_name="DECLARATIVE CLASS INSTANTIATION",
        value_label="Nepřípustná inicializace",
        expected=f"Použití '{class_name}' jako továrny/definice.",
        problem=(
            f"Třída '{class_name}' je deklarativní předpis (blueprint). "
            f"Není určena k přímému vytváření instancí."
        ),
        context=f"Volání {class_name}()",
        how_to_fix=(
            f"Pro vytvoření instance musíte nejprve vygenerovat instanční třídu.",
            f"Použijte k tomu jednu z továrních metod:",
            f"  - {class_name}.CORE()    -> pro základní hodnotové jádro",
            f"  - {class_name}.INSTANCE()-> pro atomickou instanci",
            f"  - {class_name}.MIXIN()   -> pro kompozitní mixin",
            f"  - {class_name}.OBJECT()  -> pro koncový funkční objekt",
            f"Příklad: moje_instance = {class_name}.OBJECT()()"
        ),
        exception=TypeError
    )