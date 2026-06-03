def snapshot_to_dict(snapshot):
    """
    Převede snapshot (name_snake → (path, value))
    na stromovou strukturu (dict → dict → value).
    """

    result = {}

    for name_snake, (path, value) in snapshot.items():

        # Přeskočíme root objekt (path == ())
        if not path:
            continue

        # Odstraníme podtržítka z private jmen
        clean_path = tuple(part.lstrip("_") for part in path)

        # Začneme na rootu
        node = result

        # Projdeme všechny části kromě poslední
        for part in clean_path[:-1]:
            node = node.setdefault(part, {})

        # Poslední část = klíč, do kterého uložíme hodnotu
        node[clean_path[-1]] = value

    return result



def snapshot_to_dict(snapshot):
    """
    Převede snapshot (name_snake → (path, value))
    na stromovou strukturu (dict → dict → value).
    """

    result = {}

    for name_snake, (path, value) in snapshot.items():

        # Vyřízení prvního prvku
        if not path:
            result[name_snake] = value
            continue

        # Odstraníme podtržítek
        clean_path = tuple(part.lstrip("_") for part in path)


        # Pokud je více než 1 vnitřní položka
        if len(clean_path) > 1:
            for part in clean_path[:-1]:
                result = result.setdefault(part, {})

        # přidání finální položky
        result[clean_path[-1]] = value

    return result
