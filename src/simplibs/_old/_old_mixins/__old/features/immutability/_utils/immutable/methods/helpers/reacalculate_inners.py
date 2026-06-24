

def reacalculate_inners(snapshot_dict, meta, new_value):
    """Metoda pro dopočet hodnot innerů pr kompozici"""

    # Získání inners
    inners_meta = (inner.meta for inner in meta.inners)

    # Výpočet hodnot
    inners_value = meta.decompose(new_value)

    # procházení zipu meta a hodnot
    for inner_meta, inner_value in zip(inners_meta, inners_value):

        # Zápis hlavníhodnoty
        snapshot_dict[inner_meta.name_snake] = inner_value

        # Kontrola zda se nejedná o kompozici
        if not inner_meta.is_constant:
            # Rekurzivní volání
            reacalculate_inners(snapshot_dict, inner_meta, inner_value)
