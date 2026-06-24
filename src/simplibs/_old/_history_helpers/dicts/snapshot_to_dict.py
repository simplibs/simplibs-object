def snapshot_to_dict(snapshot):

    # 1. Definice proměnných
    result = {}
    last_created_key = None

    # 2. Cyklus na položky snapshotu
    for path, value in snapshot:

        # 2.1 Vyřízení kořenové hodnoty
        if not path:
            result["value"] = value
            continue

        # 2.2 Odstranění prefixů
        clean_path = tuple(key[1:] for key in path)

        # 2.3 Vyřízení pro jeden prvek
        if len(clean_path) == 1:
            key = clean_path[0]
            result[key] = value
            last_created_key = key
            continue

        # 2.4 Kontrola zda nevytváříme vnitřní slovník
        is_same_key = clean_path[-2] == last_created_key

        # 2.5 Vyřízení pro nově založený vnitřní slovník
        if is_same_key:

            # 2.5.1 Definice proměnných
            previouse_key = clean_path[-2]
            new_key = clean_path[-1]

            # 2.5.2 Načtení poslední hodnoty
            current = result
            for key in clean_path[:-2]:
                current = current[key]
            last_value = current[previouse_key]

            # 2.5.3 Přepis hodnoty na dict
            current[previouse_key] = {
                "value": last_value,
                new_key: value
            }
            last_created_key = new_key
            continue

        # 2.6 Vyřízení popožky odkazující na hodnotu
        else:

            # 2.6.1 Definice proměnných
            new_key = clean_path[-1]

            # 2.6.2 Načtení poslední položky
            current = result
            for key in clean_path[:-1]:
                current = current.setdefault(key, {})

            # Zápis nové položky s hodnotou
            current[new_key] = value
            last_created_key = new_key

    # 3. Navrácení slovníku
    return result
