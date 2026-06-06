def restore_snapshot(instance, snapshot):
    """
    Obnoví stav instance podle snapshotu.
    Snapshot má formát:
        name_snake: (path_tuple, value)
    """

    # 1. Procházení snapshotu
    for path, value in snapshot:

        # 2. Začínáme na root instanci
        target = instance

        # 3. Projdeme všechny prvky (když není žádný, použije se instance)
        for attr in path:
            target = getattr(target, attr)

        # 4. Zápis hodnoty
        object.__setattr__(target, "_value", value)