from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ........protocols.methods import ClassMethodProtocol


def validate_method_is_classmethod(
    row_method: "ClassMethodProtocol",
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, zda je metoda správně dekorována jako @classmethod.

    Tato validace předpokládá, že existence metody v __dict__ již byla
    ověřena.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Chybějící dekorátor
    ═════════════════════════════════════════════════════════════════
    Expected:  Metoda s dekorátorem '@classmethod'.
    Problem:   '{class_name}.{method_name}' chybí tento dekorátor.
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
    if not isinstance(row_method, classmethod):

        # 2. Vypočet proměných
        class_name = base_info["class_name"]
        method_name = base_info["method_name"]
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label=f"Chybějící dekorátor",
            expected="Metoda s dekorátorem '@classmethod'.",
            problem=f"'{class_name}.{method_name}' chybí tento dekorátor.",
            context=context,
            how_to_fix=(
                "Přidejte dekorátor '@classmethod' k metodě '{method_name}'.",
                "Bez tohoto dekorátoru nemůže systém správně analyzovat její parametry.",
            ) + expected_structure,
            exception=TypeError
        )
