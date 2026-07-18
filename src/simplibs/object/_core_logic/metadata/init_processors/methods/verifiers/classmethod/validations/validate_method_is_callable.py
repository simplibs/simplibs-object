from collections.abc import Callable
# Outers
from ........exceptions import SimpleMetadataError


def validate_method_is_callable(
    row_method: Callable,
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, že atribut třídy je volatelný objekt (callable).

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Metoda není volatelný objekt
    ═════════════════════════════════════════════════════════════════
    Expected:  Volatelná třídní metoda.
    Problem:   '{class_name}.{method_name}' není volatelná.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Ujistěte se, že '{method_name}' je definovaná jako metoda.
         • Zkontrolujte, že není nahrazen datovým atributem.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not callable(row_method):

        # 2. Vypočet proměných
        class_name = base_info["class_name"]
        method_name = base_info["method_name"]
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Metoda není volatelný objekt",
            expected="Volatelná třídní metoda.",
            problem=f"'{class_name}.{method_name}' není volatelný objekt.",
            context=context,
            how_to_fix=(
                f"Ujistěte se, že '{method_name}' je definovaná jako metoda.",
                "Zkontrolujte, že není nahrazen datovým atributem.",
            ) + expected_structure,
            exception=TypeError
        )