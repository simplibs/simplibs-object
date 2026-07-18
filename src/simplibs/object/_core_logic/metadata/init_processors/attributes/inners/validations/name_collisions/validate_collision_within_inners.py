from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMetadataError
from .._exceptions_helpers import exception_info_for_inners
# Inners
from .utils import get_collision_path
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike


def validate_collision_within_inners(
    collision_name: str,
    owner_snake_name: str,
    raw_inners: tuple["SimpleClassLike", ...],
    current_inner: "SimpleClassLike",
    owner_class: "SimpleClassLike"
) -> None:
    """
    Identifikuje zdroj kolize mezi vnitřními prvky a vyvolá detailní výjimku
    označující prvek, který jméno do kompozice přinesl jako první.

    ═════════════════════════════════════════════════════════════════
    ⚠️ INVALID INNERS DEFINITION: Kolize jmen v _inners
    ═════════════════════════════════════════════════════════════════
    Expected:  Unikátní názvy (name_snake) pro všechny prvky v hierarchii.
    Problem:   Byla nalezena kolize jména '{collision_name}' mezi dvěma vnitřními prvky kompozice.
    Context:   Kontrola a validace metadat pro: {class_name}.{attribute_name}
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • Kolizní jméno: '{collision_name}'.
         • Cesta k prvnímu viníkovi: {first_culprit_full_path}.
         • Cesta k druhému viníkovi: {second_culprit_full_path}.
         • Přejmenujte jeden z kolizních prvků tak, aby byl v rámci '{class_name}' unikátní.
         • Zkontrolujte, zda nedošlo k duplicitnímu vložení stejné třídy do '_inners'.
         • Pamatujte, že name_snake se tvoří z názvu třídy a ten se nesmí opakovat v celém stromu této třídy.
    ═════════════════════════════════════════════════════════════════
    """

    # 1. Podmínka výjimky
    if collision_name and collision_name != owner_snake_name:

        # 2. Vypočet proměných
        (class_name,
         error_name,
         context,
         acceptable_definitions
         ) = exception_info_for_inners(owner_class)

        # Získání cesty k prvnímu viníkovi (včetně názvu vlastnické třídy na začátku)
        first_culprit_path = None
        for previous_inner in raw_inners:
            if collision_name in previous_inner.meta.node_names_set:
                first_culprit_path = get_collision_path(previous_inner, collision_name)
                break
        first_culprit_full_path = f"{class_name} -> {first_culprit_path}"

        # Získání cesty k druhému viníkovi (včetně názvu vlastnické třídy na začátku)
        second_culprit_path = get_collision_path(current_inner, collision_name)
        second_culprit_full_path = f"{class_name} -> {second_culprit_path}"

        # 4. Vyvolání výjimky
        raise SimpleMetadataError(
            error_name=error_name,
            label="Kolize jmen v _inners",
            expected="Unikátní názvy tříd pro všechny prvky v hierarchii.",
            problem=f"Byla nalezena kolize jména mezi dvěma vnitřními prvky kompozice.",
            context=context,
            how_to_fix=(
                f"Kolizní jméno: '{collision_name}'.",
                f"Cesta k prvnímu viníkovi: {first_culprit_full_path}.",
                f"Cesta k druhému viníkovi: {second_culprit_full_path}.",
                f"Přejmenujte jeden z kolizních prvků tak, aby byl v rámci '{class_name}' unikátní.",
                "Zkontrolujte, zda nedošlo k duplicitnímu vložení stejné třídy do '_inners'."
                "Pamatujte, že name_snake se tvoří z názvu třídy a ten se nesmí opakovat v celém stromu této třídy.",
            ),
            exception=NameError
        )


_DESIGN_NOTES_INNERS = """
# validate_collision_within_inners

## Účel
Tato funkce je volána v momentě, kdy je prokázána duplicita jmen v rámci `_inners`, 
ale bylo již vyloučeno, že by šlo o kolizi s vlastníkem. Jejím úkolem je 
introspekce seznamu `_inners` a nalezení "prvotního hříšníka".

## Strategie "Prstem na viníka"
Protože `_inners` je neměnný tuple a my ho procházíme ve stejném pořadí, v jakém 
vznikal set `node_names_set`, je zaručeno, že první nalezený výskyt jména v podstromu 
některého z prvků je ten, který způsobil původní obsazení jména.

## Sémantika
Tato funkce na rozdíl od své sestry neprovádí žádnou podmíněnou kontrolu – 
předpokládá se, že pokud byla zavolána, kolize existuje. Proto na konci 
vždy vyvolá výjimku. Rozbití na tuto samostatnou funkci umožňuje udržet 
hlavní validační cyklus extrémně stručný a čitelný.
"""