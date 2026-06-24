def reacalculate_owner_value(snapshot_dict, owner):
    """Metoda pro dopočet pomoziční hodnoty na základě hodnot jeho innerů"""

    # Načtení přímých innerů
    owner_inners_name = (inner.meta.name_snake for inner in owner.meta.inners)

    # Vytvoření slovníku s hodnotami
    owner_inners_value_dict = {name: snapshot_dict[name] for name in owner_inners_name}

    # Výpočet nové hodnoty kompozice
    new_value = owner.logic(*owner_inners_value_dict)

    # Zápis nové hodnoty kompozice
    snapshot_dict[owner.meta.name_snake] = new_value