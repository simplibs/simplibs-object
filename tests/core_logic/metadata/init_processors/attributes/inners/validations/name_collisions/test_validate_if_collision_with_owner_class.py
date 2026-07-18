from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exceptions_helpers import exception_info_for_inners
# Inners
from .utils import get_collision_path
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_if_collision_with_owner_class(
    collision_name: str,
    owner_snake_name: str,
    inner_culprit: type,
    owner_class: "SimpleClassLike"
) -> None:
    """
    Prověří, zda kolizní jméno neodpovídá jménu samotné vlastnické třídy.
    Pokud ano, vyvolá specifickou výjimku pro kolizi s vlastníkem.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Name colision with owner
    ═════════════════════════════════════════════════════════════════
    Expected:  Unikátní názvy třídy v rámci celé hierarchie objektu.
    Problem:   Vnitřní prvek kompozice má stejné jméno jako jeho vlastník.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Kolizní jméno: '{collision_name}'.
         • Cesta k viníkovi: {full_path}.
         • Přejmenujte třídu '{culprit_path.split('/')[-1]}' v podstromu kompozice.
         • Nebo přejmenujte samotnou vlastnickou třídu '{class_name}'.
         • Každá třída v hierarchii musí mít unikátní 'name_snake'.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if collision_name == owner_snake_name:

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # Získání cesty k viníkovi (včetně názvu vlastnické třídy na začátku)
        culprit_path = get_collision_path(inner_culprit, collision_name)
        full_path = f"{class_name} -> {culprit_path}"

        # 3. Vyovlání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            label="Name colision with owner",
            expected="Unikátní názvy třídy v rámci celé hierarchie objektu.",
            problem="Vnitřní prvek kompozice má stejné jméno jako jeho vlastník.",
            context=context,
            how_to_fix=(
                f"Kolizní jméno: '{collision_name}'.",
                f"Cesta k viníkovi: {full_path}.",
                f"Přejmenujte třídu '{culprit_path.split('/')[-1]}' v podstromu kompozice.",
                f"Nebo přejmenujte samotnou vlastnickou třídu '{class_name}'.",
                "Každá třída v hierarchii musí mít unikátní 'name_snake'."
            ),
            exception=NameError
        )

_DESIGN_NOTES_OWNER = """
# validate_if_collision_with_owner_class

## Účel
Tato funkce řeší nejzávažnější typ kolize – situaci, kdy se vnořený prvek (nebo jeho 
potomek) jmenuje stejně jako třída, která ho obsahuje. 

## Logika
Funkce je navržena jako "pasivní strážce". Pokud `collision_name` neodpovídá 
vlastníkovi, funkce mlčky skončí a umožní pipeline pokračovat k dalšímu kroku. 
Tím je v hlavní smyčce dosaženo čistého lineárního toku bez složitého větvení.

## Proč odděleně?
Kolize s vlastníkem má jinou sémantiku a jiné řešení než kolize mezi sourozenci. 
Oddělením do vlastní funkce můžeme uživateli poskytnout velmi přesné instrukce 
k opravě, které se zaměřují na hierarchický vztah rodič-dítě.
"""