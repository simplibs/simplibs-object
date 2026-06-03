def diff_snapshots(snap1, snap2, leaves_only=False):

    # 1. Vtyvoření proměných
    diffs = []
    last_path = None

    # 2. Cyklus skrtze oba snapshoty
    for (path, snap1_val), (_, snap2_val) in zip(snap1, snap2):

        # 2.1 Pokud hodnoty jsou stejné → pokračujeme dále
        if snap1_val == snap2_val:
            continue

        # 2.2 Pokud leaves_only=False → rovnou přidáme
        if not leaves_only:
            diffs.append((path, snap1_val, snap2_val))
            continue

        # 2.3 Pokud leaves_only=True
        # Kontrola zda ancestor existuje a je ze stejné větve
        if (last_path is not None and
            path[:len(last_path)] == last_path):

            # 2.3.1 Pokud ano ahradíme ancestor aktuálním leafem
            diffs[-1] = (path, snap1_val, snap2_val)
            last_path = path

        else:
            # 2.3.2 Pokud ne, pak zapíšeme a přidáme mezi ancestory
            diffs.append((path, snap1_val, snap2_val))
            last_path = path

    # 3. Navrácení tuple se změnami
    return tuple(diffs)


