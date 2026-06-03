from typing import Any
# Outers
from .....exceptions import SimpleObjectMetadataError
from ...utils import exception_context_for_classmethod


def validate_bound_method_outcome_type(
    calculated_value: Any,
    expected_return_type: type,
    bound_method: classmethod,
) -> None:
    """
    Validuje, že hodnota vrácená zkušebním výpočtem odpovídá očekávanému typu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Neplatný typ výsledku výpočtu
    ═════════════════════════════════════════════════════════════════
    Expected:  Návratová hodnota typu '{expected_return_type.__name__}'.
    Got:       {repr(calculated_value)} ({type(calculated_value).__name__})
    Problem:   Výsledek metody '{method_name}' neodpovídá definovanému typu.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Chybu může působit logika metody, nebo definice typu, dle kterého se logika ověřuje.
         • {type_definition.get(method_name, '')}
         • Buď upravte logiku metody tak, aby vracela typ '{expected_return_type.__name__}'.
         • Nebo upravte definici typu, aby odpovídal vypočtené hodnotě '{type(calculated_value.__name__)}'.
         • Example:
         •     @classmethod
         •     def {method_name}(cls, ...) -> {expected_return_type.__name__}:
         •         return ...  # Musí být instance {expected_return_type.__name__}
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not isinstance(calculated_value, expected_return_type):

        # 2. Výpočet proměnných
        class_name, method_name, context = exception_context_for_classmethod(bound_method)
        type_definition = {
            "_logic": f"Návratová hodnota by měla odpovídat definici '{class_name}._type'.",
            "_decompose": f"Návratová hodnota by měla být tuple a odpovídat počtem položek a typům '{class_name}._inners'.",
            "_validate": "Návratová hodnota by měla být 'bool', nebo 'None', nebo 'bool | None'"
        }

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD LOGIC ERROR",
            value_label="Neplatný typ výsledku výpočtu",
            expected=f"Návratová hodnota typu '{expected_return_type.__name__}'.",
            value=calculated_value,
            problem=f"Výsledek metody '{method_name}' neodpovídá očekávanému typu.",
            context=context,
            how_to_fix=(
                f"Chybu může působit logika metody, nebo definice typu, dle kterého se logika ověřuje.",
                f"{type_definition.get(method_name, '')}",
                f"Buď upravte logiku metody tak, aby vracela typ '{expected_return_type.__name__}'.",
                f"Nebo upravte definici typu, aby odpovídal vypočtené hodnotě '{type(calculated_value).__name__}'.",
                "Example:",
                "    @classmethod",
                f"    def {method_name}(cls, ...) -> {expected_return_type.__name__}:",
                f"        return ...  # Musí být instance {expected_return_type.__name__}"
            ),
            exception=TypeError
        )