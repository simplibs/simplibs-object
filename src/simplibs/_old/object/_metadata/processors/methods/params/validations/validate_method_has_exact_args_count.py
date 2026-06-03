from typing import Callable
# Outers
from .....exceptions import SimpleObjectMetadataError


def validate_method_has_exact_args_count(
    expected_args_count: int,
    actual_args_count: int,
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje počet pozičních parametrů (co_argcount).

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD SIGNATURE ERROR: Nesprávný počet pozičních parametrů
    ═════════════════════════════════════════════════════════════════
    Expected:  Počet pozičních parametrů: {expected_args_count}
    Problem:   Obdržený počet pozičních parametrů: {expected_args_count}
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}.
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Zkontrolujte, zda jste za 'cls' uvedli všechny potřebné parametry.
         • Ověřte zda vaše definice odpovídá očekávané definici.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """
    # 1. Podmínka výjimky
    if actual_args_count != expected_args_count:

        # 2. Vypočet proměných
        excepted_structure = base_info["excepted_structure"]
        context = base_info["context"]

        # 3. Vyvolání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD SIGNATURE ERROR",
            value_label="Nesprávný počet pozičních parametrů",
            expected=f"Počet pozičních parametrů: {expected_args_count}",
            problem=f"Obdržený počet pozičních parametrů: {expected_args_count}",
            context=context,
            how_to_fix=(
                f"Zkontrolujte, zda jste za 'cls' uvedli všechny potřebné parametry.",
                "Ověřte zda vaše definice odpovídá očekávané definici."
            ) + excepted_structure,
            exception=TypeError
        )