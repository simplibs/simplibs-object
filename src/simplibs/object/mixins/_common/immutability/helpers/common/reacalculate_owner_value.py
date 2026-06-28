from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ......protocols.instance import SimpleInstanceLike
    from ......protocols.alias_typings import SnapshotDict


def reacalculate_owner_value(
    snapshot_dict: "SnapshotDict",
    owner: "SimpleInstanceLike"
) -> None:
    """Metoda pro dopočet pomoziční hodnoty na základě hodnot jeho innerů"""

    # 1. Načtení přímých innerů
    owner_inners_name = (inner.meta.name_snake for inner in owner.meta.inners)

    # 2. Vytvoření slovníku s hodnotami
    owner_inners_value_dict = {name: snapshot_dict[name] for name in owner_inners_name}

    # 3. Výpočet nové hodnoty kompozice
    new_value = owner.logic(*owner_inners_value_dict)

    # 4. Zápis nové hodnoty kompozice
    snapshot_dict[owner.meta.name_snake] = new_value