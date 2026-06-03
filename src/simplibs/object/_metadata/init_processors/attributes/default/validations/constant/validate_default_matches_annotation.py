from typing import Any
# Outers
from .......exceptions import SimpleMetadataError
from ......._types import SimpleClassType
from .._exceptions_helpers import exception_info_for_default


def validate_default_matches_annotation(
    default_value: Any,
    expected_type: Any,
    owner_class: SimpleClassType,
) -> None:
    """
    Validuje, že hodnota '_default' odpovídá definovanému typu '_type'.

    Využívá funkci isinstance, která si díky předchozím validacím poradí
    s atomickými typy, Uniony i plochými tuply.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID DEFAULT DEFINITION: Hodnota neodpovídá anotaci
    ═════════════════════════════════════════════════════════════════
    Expected:  Hodnota typu: {expected_type}.
    Got:       repr(value) (type)
    Problem:   Definovaný default neodpovídá definovanému typu.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Změňte hodnotu '_default' tak, aby odpovídala typu '{expected_type}'.
         • Nebo upravte definici '_type' tak, aby zahrnovala aktuální typ hodnoty.
         • U konstanty (SimpleConstant) je definice platného '_default' povinná.
    ═════════════════════════════════════════════════════════════════
    """
    # 1. Podmínka výjimky
    if not isinstance(default_value, expected_type):

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         ) = exception_info_for_default(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label="Hodnota neodpovídá anotaci",
            expected=f"Hodnota typu: {expected_type}",
            value=default_value,
            problem="Definovaný default neodpovídá definovanému typu.",
            context=context,
            how_to_fix=(
                f"Změňte hodnotu '_default' tak, aby odpovídala typu '{expected_type}'.",
                "Nebo upravte definici '_type' tak, aby zahrnovala aktuální typ hodnoty.",
                "U konstanty (SimpleConstant) je definice platného '_default' povinná."
            ),
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_default_matches_annotation

## Účel
Tato validace propojuje definici typu se skutečnou hodnotou. Je to klíčový bod 
pro zachování typové bezpečnosti celého SimpleObject systému.

## Spolupráce s předchozími kroky
Díky tomu, že `validate_type_definition` již zajistil, že `_type` je validní 
vstup pro `isinstance()`, zde můžeme bezpečně a rychle provést typovou kontrolu.

## Význam pro uživatele
Zabráníme vzniku logických chyb, kdy uživatel deklaruje, že objekt reprezentuje 
`int`, ale jako výchozí hodnotu podstrčí `str`. Tím garantujeme, že `_logic` 
v budoucnu (nebo přímé použití defaultu) nikdy nevrátí neočekávaný typ dat.
"""