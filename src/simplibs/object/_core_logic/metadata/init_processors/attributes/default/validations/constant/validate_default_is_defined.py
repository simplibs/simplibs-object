from typing import Any
from simplibs.sentinels import UNSET
# Outers
from .......exceptions import SimpleMetadataError
from .......protocols import SimpleClassType
from .._exceptions_helpers import exception_info_for_default


def validate_default_is_defined(
    default_value: Any,
    owner_class: SimpleClassType
) -> None:
    """
    Validuje, že atribut '_default' byl definován.

    Tato kontrola se spouští pouze ve větvi konstanty (pokud nejsou _default).
    Vynucuje, aby každá konstanta měla jasně danou výchozí hodnotu.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID DEFAULT DEFINITION: Attribut není definovaný
    ═════════════════════════════════════════════════════════════════
    Expected:  Attribut '_default' obsahující výchozí hodnotu konstanty.
    Problem:   Attribut není na třídě nedefinovaný.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Třída konstanty (SimpleConstant) musí deklarovat attribut '_default'.
         • Doplňte atribut '_default' do definice třídy..
         • Pokud měl být objekt kompozicí (SimpleObject), doplňte atribut '_inners' a metodu '_logic'.
         • Zkontrolujte, zda jste omylem nesmazali výchozí hodnotu z definice.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if default_value is UNSET:

        # 2. Vypočet proměných
        (class_name,
         class_parrent,
         error_name,
         context,
         ) = exception_info_for_default(owner_class)

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            value_label="Attribut '_default' není definovaný",
            expected=f"Attribut '_default' obsahující výchozí hodnotu konstanty.",
            problem=f"Attribut není na třídě nedefinovaný.",
            context=context,
            how_to_fix=(
                "Třída konstanty (SimpleConstant) musí deklarovat attribut '_default'.",
                "Doplňte atribut '_default' do definice třídy.",
                "Pokud měl být objekt kompozicí, doplňte atribut '_inners' a metodu '_logic'.",
                "Zkontrolujte, zda jste omylem nesmazali výchozí hodnotu z definice."
            ),
            exception=ValueError
        )


_DESIGN_NOTES = """
# validate_default_is_defined

## Účel
Zajišťuje, že žádný objekt typu SimpleObject nezůstane v "nedefinovaném" stavu. 
Pokud objekt neobsahuje vnitřní prvky (není kompozicí), systém ho automaticky 
považuje za konstantu a vyžaduje pro něj pevnou hodnotu.

## Proč UNSET a ne None?
Používáme naši konstantu `UNSET`, protože `None` může být v jiných systémech 
validní hodnotou. My ale chceme vědět, zda uživatel hodnotu *opravdu zapomněl*.

## Role v rozhodovacím stromu
Tato validace funguje jako záchranná síť. Pokud uživatel nevytvořil kompozici 
a zároveň zapomněl na default, tato zpráva ho navede k oběma možným opravám.
"""