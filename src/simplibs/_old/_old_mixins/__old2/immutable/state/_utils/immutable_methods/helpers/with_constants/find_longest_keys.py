def find_longest_keys(path_dict):

    # 1. Převedeme slovník na seznam dvojic (klíč, cesta)
    # a seřadíme ho podle CESTY (položka na indexu 1)
    sorted_path = sorted(path_dict.items(), key=lambda x: x[1])
    longest_keys = []

    # 2. Procházíme a porovnáváme cesty mezi sebou
    for i in range(len(sorted_path) - 1):
        key, path = sorted_path[i]
        _, next_path = sorted_path[i + 1]

        # Pokud následující cesta začíná tou aktuální,
        # aktuální je jen mezikrok a přeskočíme ji.
        if next_path[:len(path)] == path:
            continue

        # Pokud nezačíná, máme tu koncový bod! Uložíme jeho klíč.
        longest_keys.append(key)

    # Poslední prvek v seřazeném seznamu je vždycky koncový
    longest_keys.append(sorted_path[-1][0])

    return tuple(longest_keys)