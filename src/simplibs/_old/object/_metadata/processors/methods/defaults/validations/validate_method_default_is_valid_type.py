from typing import Any
# Outers
from .....exceptions import SimpleObjectMetadataError
from ...utils import exception_context_for_classmethod


def validate_method_default_is_valid_type(
    value: Any,
    expected_type: type,
    bound_method: classmethod,
) -> None:
    """
    Validuje, že uživatelem definovaná defaultní hodnota parametru
    odpovídá očekávanému typu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Neplatný typ defaultní hodnoty
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota typu '{expected_type.__name__}'.
    Got:       {repr(value)} ({type(value).__name__})
    Problem:   Defaultní hodnota parametru neodpovídá typu definovanému v '_inners'.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Změňte defaultní hodnotu tak, aby odpovídala typu '{expected_type.__name__}'.
         • Pokud má parametr přijímat tento typ, ověřte definici v '_inners'.
         • Example:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}(cls, ..., param: {expected_type.__name__} = správná_hodnota):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not isinstance(value, expected_type):

        # 2. Vypočet proměných
        class_name, method_name, context = exception_context_for_classmethod(bound_method)

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            value_label="Neplatný typ defaultní hodnoty",
            expected=f"Hodnota typu '{expected_type.__name__}'.",
            value=value,
            problem="Defaultní hodnota parametru neodpovídá typu definovanému v '_inners'.",
            context=context,
            how_to_fix=(
                f"Změňte defaultní hodnotu tak, aby odpovídala typu '{expected_type.__name__}'.",
                f"Pokud má parametr přijímat tento typ, ověřte definici v '_inners'.",
                "Example:",
                f"class {class_name}(SimpleObject):",
                "    ...",
                "    @classmethod",
                f"    def {method_name}(cls, ..., param: {expected_type.__name__} = ...):"
                "        ..."
            ),
            exception=TypeError
        )