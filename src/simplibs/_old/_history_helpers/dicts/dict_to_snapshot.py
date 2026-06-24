def dict_to_snapshot(snapshot_dict):
    """
    Převede dict (vytvořený pomocí snapshot_to_dict) zpět na snapshot.
    Snapshot má formát: tuple of (path_tuple, value)
    """

    # 1. Definice seznamu
    snapshot = []

    # 2. Rekurzivní pomocná funkce
    def _collect(processed_dict, path):

        # 2.1 Kořenová nebo vnitřní hodnota
        if "value" in processed_dict:
            snapshot.append((path, processed_dict["value"]))

        # 2.2 Procházení ostatních klíčů
        for key, val in processed_dict.items():

            # 2.3 Přeskočení klíče value (ten jsme zpracovali výše)
            if key == "value":
                continue

            # 2.4 Rekonstrukce původního názvu s prefixem
            private_key = "_" + key
            new_path = path + (private_key,)

            # 2.5 Vyřízení zanořené kompozice → rekurze
            if isinstance(val, dict):
                _collect(val, new_path)

            # 2.6 Vyřízení skalární hodnota → přímý zápis
            else:
                snapshot.append((new_path, val))

    # 3. Spuštění rekurze od kořene
    _collect(snapshot_dict, ())

    # 4. Navrácení tuple
    return tuple(snapshot)