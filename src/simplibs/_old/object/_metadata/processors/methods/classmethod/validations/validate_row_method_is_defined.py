# Outers
from ......exceptions import SimpleObjectMetadataError
from ......_types import SimpleClassType


def validate_row_method_is_defined(
    method_name: str,
    owner_class: SimpleClassType,
    base_info: dict[str, str | tuple[str, ...]],
) -> None:
    """
    Validuje, že třída má určitou metodu.

    Kontrola probíhá skrze __dict__, aby bylo zajištěno, že potomek metodu
    skutečně implementoval a nespoléhá se na výchozí (prázdnou) implementaci.

    ═════════════════════════════════════════════════════════════════
    ⚠️ METHOD LOGIC ERROR: Chybějící dekorátor
    ═════════════════════════════════════════════════════════════════
    Expected:  Třídní metoda '{method_name}()'.
    Problem:   Třídě '{class_name}' chybí tato metoda.
    Context:   Kontrola a validace metadat pro: {class_name}.{method_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Doplňte metodu '{method_name}' do definice třídy '{class_name}'.
         • Metoda musí být dekorována jako @classmethod.
         • Její parametry musí odpovídat definovaným '_inners'.
         • Expected structure:
         • class {class_name}(SimpleObject):
         •     ...
         •     @classmethod
         •     def {method_name}({', '.join(expected_params)}):
         •         ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if method_name not in owner_class.__dict__:

        # 2. Vypočet proměných
        class_name = base_info["class_name"]
        excepted_structure = base_info["excepted_structure"]
        context = base_info["context"]

        # 3. Vyovlání výjimky
        raise SimpleObjectMetadataError(
            error_name="METHOD LOGIC ERROR",
            value_label="Chybějící metoda",
            expected=f"Třídní metoda '{method_name}()'.",
            problem=f"Třídě '{class_name}' chybí tato metoda.",
            context=context,
            how_to_fix=(
                f"Doplňte metodu '{method_name}' do definice třídy '{class_name}'.",
                "Metoda musí být dekorována jako @classmethod."
                "Její parametry musí odpovídat definovaným '_inners'.",
            ) + excepted_structure,
            exception=AttributeError
        )