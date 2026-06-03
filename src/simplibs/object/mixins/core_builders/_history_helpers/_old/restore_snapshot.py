def restore_snapshot(instance, snapshot):
    """
    Obnoví stav instance podle snapshotu.
    Snapshot má formát:
        name_snake: (path_tuple, value)
    """

    for path, value in snapshot.values():

        # Začínáme na root instanci
        target = instance

        # Projdeme všechny prvky (když není žádný, použije se instance)
        for attr in path:
            target = getattr(target, attr)

        # Zápis hodnoty
        object.__setattr__(target, "_value", value)