from typing import Callable
# Outers
from .....exceptions import SimpleObjectMetadataError

def validate_method_not_use_param_placeholders(
    has_varargs: bool,
    has_varkwargs: bool,
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, že metoda nepoužívá variabilní parametry (*args, **kwargs).

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Chybějící dekorátor
    ═════════════════════════════════════════════════════════════════
    Expected:  Třídní metoda 'method_name()'.
    Problem:   Třídě 'MyClass' chybí tato metoda.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Přidejte dekorátor '@classmethod' k metodě '{method_name}'.
         • Bez tohoto dekorátoru nemůže systém správně analyzovat její parametry.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """
    # 1. Podmínka výjimky
    if has_varargs or has_varkwargs:

        # 2. Výpočet proměnných
        class_name = base_info["class_name"]
        method_name = base_info["method_name"]
        excepted_structure = base_info["excepted_structure"]
        context = base_info["context"]
        problem_type = []
        if has_varargs: problem_type.append("*args")
        if has_varkwargs: problem_type.append("**kwargs")

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            value_label="Zakázané variabilní parametry",
            expected="Explicitně pojmenované parametry.",
            problem=f"Metoda '{class_name}.{method_name}' používá {', '.join(problem_type)}.",
            context=context,
            how_to_fix=(
                f"Odstraňte '{', '.join(problem_type)}' z definice metody.",
                "Všechny parametry musí být vypsány jmenovitě podle jejich sémantického významu."
            ) + excepted_structure,
            exception=TypeError
        )