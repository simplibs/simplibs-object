from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exceptions_helpers import exception_info_for_inners
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_inner_is_class(
    inner: "SimpleClassLike",
    inners: tuple["SimpleClassLike", ...],
    owner_class: "SimpleClassLike"
) -> None:
    """
    Validuje, zda je prvek v '_inners' skutečně datovým typem (třídou).

    Toto je nultý krok validace prvků kompozice, který zajišťuje,
    že pracujeme s definicemi, nikoliv s jejich instancemi nebo daty.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Prvek z _inners není platná třída
    ═════════════════════════════════════════════════════════════════
    Expected:  Vnitřní prvek musí být třída (potomek SimpleObject/SimpleConstant).
    Got:       repr(inner) (type)
    Problem:   Vnitřní prvek '{inner}' z '{inners}' není validním objektem.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Vnitřní prvky atributu _inners mohou být pouze potomci třídy SimpleObject a SimpleConstant.
         • Opravte uvedený prvek, tak aby byl validním prvkem.
         • Do seznamu '_inners' vkládejte pouze odkazy na třídy, nikoliv jejich instance nebo jiné datové typy.
         • Ujistěte se, že prvek není např. řetězec nebo výsledek volání funkce.
         • Acceptable definitions:
         • class {class_name}(class_parrent):
         •     _inners: tuple = (PrvekA, PrvekB)
         •     ...
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if not isinstance(inner, type):

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            label="Prvek z _inners není platná třída",
            value=inner,
            expected="Vnitřní prvek musí být třída (potomek SimpleObject/SimpleConstant).",
            problem=f"Vnitřní prvek '{inner}' z '{inners}' není validním objektem.",
            context=context,
            how_to_fix=(
                "Vnitřní prvky atributu _inners mohou být pouze potomci třídy SimpleObject a SimpleConstant.",
                "Opravte uvedený prvek, tak aby byl validním prvkem.",
                "Do seznamu '_inners' vkládejte pouze odkazy na třídy, nikoliv jejich instance nebo jiné datové typy.",
                "Ujistěte se, že prvek není např. řetězec nebo výsledek volání funkce.",
            ) + acceptable_definitions,
            exception=TypeError
        )


_DESIGN_NOTES = """
# validate_inner_is_class

## Účel
Tato validace slouží jako "vstupní filtr" pro integritu kompozice. Jejím hlavním 
úkolem je zajistit, že každý prvek v seznamu `_inners` je typem (`type`), 
tedy popisem struktury, nikoliv strukturou samotnou (instancí).

## Proč je tato kontrola nutná jako první?
1. **Ochrana následných validací**: Funkce jako `issubclass` nebo přístup k 
   atributům přes `.meta` (který očekáváme u SimpleObjectů) vyžadují, aby 
   vstupem byla třída. Pokud by sem prošla instance, systém by havaroval na 
   nepřehledné systémové chybě místo naší strukturované výjimky.
2. **Prevence běžné chyby**: Uživatelé často píší závorky tam, kde nemají. 
   Tato validace okamžitě odhalí záměnu `Vaha()` (instance) za `Vaha` (třída).

## Explicitnost vs. Try-Except
Zvolili jsme explicitní volání `isinstance(inner, type)` namísto odchytávání 
výjimek v pozdějších krocích. Tento přístup umožňuje poskytnout uživateli 
velmi specifickou nápovědu (`how_to_fix`) zaměřenou čistě na chybný datový 
typ vstupu, což zvyšuje "vnitřní zen" při ladění kódu.
"""