from typing import TYPE_CHECKING, Any
# Outers
from ........exceptions import SimpleMetadataError
from .._exceptions_helpers import exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inners_is_tuple(
    inners: Any,
    owner_class: "SimpleClassLike"
) -> None:
    """
    Validuje, že '_inners' jsou definovány jako 'tuple'.

    Tato kontrola předchází chybám při iteraci a zajišťuje neměnnost 
    definice struktury kompozitního objektu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Atribut neodkazuje na tuple
    ═════════════════════════════════════════════════════════════════
    Expected:  "N-tice (tuple) obsahující potomky tříd SimpleConstant a SimpleObject."
    Got:       repr(value) (type)
    Problem:   Atribut '_inners' není definován jako tuple.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Změňte definici '_inners' na tuple.
         • Příklad: _inners = (PrvekA, PrvekB).
         • Pokud máte pouze jeden prvek, nezapomeňte na čárku: _inners = (PrvekA,).
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _inners: tuple = (PrvekA, PrvekB)
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not isinstance(inners, tuple):

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label=f"Atribut neodkazuje na tuple",
            expected="N-tice (tuple) obsahující potomky tříd SimpleConstant a SimpleObject.",
            value=inners,
            problem=f"Atribut '_inners' musí být definován jako tuple.",
            context=context,
            how_to_fix=(
                "Změňte definici '_inners' na tuple.",
                "Příklad: _inners = (PrvekA, PrvekB).",
                "Pokud máte pouze jeden prvek, nezapomeňte na čárku: _inners = (PrvekA,)."
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