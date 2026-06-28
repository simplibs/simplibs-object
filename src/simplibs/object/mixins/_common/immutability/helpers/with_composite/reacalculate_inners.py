from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike
    from ......protocols.alias_typings import SnapshotDict


def reacalculate_inners(
    snapshot_dict: "SnapshotDict",
    meta: "SimpleMetadataLike",
    new_value: Any
) -> None:
    """Metoda pro dopočet hodnot innerů pr kompozici"""

    # 1. Získání inners
    inners_meta = (inner.meta for inner in meta.inners)

    # 2. Výpočet hodnot
    inners_value = meta.decompose(new_value)

    # 3. Procházení zipu meta a hodnot
    for inner_meta, inner_value in zip(inners_meta, inners_value):

        # 3.1 Zápis hlavníhodnoty
        snapshot_dict[inner_meta.name_snake] = inner_value

        # 3.2 Kontrola zda se nejedná o kompozici
        if not inner_meta.is_constant:
            # Rekurzivní volání
            reacalculate_inners(snapshot_dict, inner_meta, inner_value)
