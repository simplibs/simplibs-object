from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_method_is_defined(
    method_name: str,
    owner_class: "SimpleClassLike",
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
        expected_structure = base_info["expected_structure"]
        context = base_info["context"]

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name="METHOD LOGIC ERROR",
            label="Chybějící metoda",
            expected=f"Třídní metoda '{method_name}()'.",
            problem=f"Třídě '{class_name}' chybí tato metoda.",
            context=context,
            how_to_fix=(
                f"Doplňte metodu '{method_name}' do definice třídy '{class_name}'.",
                "Metoda musí být dekorována jako @classmethod."
                "Její parametry musí odpovídat definovaným '_inners'.",
            ) + expected_structure,
            exception=AttributeError
        )