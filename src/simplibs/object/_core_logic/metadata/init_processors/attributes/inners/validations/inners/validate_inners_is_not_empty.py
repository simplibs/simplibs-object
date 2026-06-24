from typing import Any
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_inners


def validate_inners_is_not_empty(
    inners: Any,
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že '_inners' není prázdným objektem.

    Tato kontrola předchází chybám při iteraci a zajišťuje neměnnost 
    definice struktury kompozitního objektu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Atribut is empty tuple
    ═════════════════════════════════════════════════════════════════
    Expected:  "N-tice (tuple) obsahující potomky tříd SimpleConstant a SimpleObject."
    Got:       repr(value) (type)
    Problem:   Atribut '_inners' nesmí být prázdný.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Zajistěte aby byla definice '_inners' správně definovaná.
         • Atribut '_inners' musí být definován jako tuple a nesmí být prázdný.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _inners: tuple = (PrvekA, PrvekB)
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if isinstance(inners, tuple) and not inners:

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label=f"{owner_class.__name__}._inners",
            expected="N-tice (tuple) obsahující potomky tříd SimpleConstant a SimpleObject.",
            value=inners,
            problem=f"Atribut '_inners' odkazuje na prázdný objekt.",
            context=context,
            how_to_fix=(
                "Zajistěte aby byla definice '_inners' správně definovaná.",
                "Atribut '_inners' musí být definován jako tuple a nesmí být prázdný."
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inners_is_tuple

## Účel
Tato validace je první kontrolou v procesu kompozice. Vynucuje použití datového 
typu `tuple` pro definici vnitřních prvků `_inners`.

## Proč právě Tuple?
1. **Imutabilita**: Definice třídy by měla být konstantní. Tuple dává jasně 
   najevo, že se seznam prvků nebude za běhu měnit.
2. **Konzistence**: Na rozdíl od setu (množiny) zachovává tuple pořadí prvků, 
   což je kritické pro pořadí parametrů v automaticky generované signatuře `_logic`.
3. **Konvence**: V Pythonu je zvykem používat tuple pro typové anotace a 
   strukturální definice (např. `isinstance` také přijímá tuple).

## Častá chyba (Edge Case)
Uživatelé často zapomínají, že jednoprvkový tuple vyžaduje čárku `(Prvek,)`. 
Bez ní Python závorky interpretuje jen jako prioritu operací a vrátí samotný 
objekt uvnitř. Tato validace tuto chybu okamžitě zachytí.
"""