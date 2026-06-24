def _collect_nodes_data(instance, path, nodes_list):
    """
    Rekurzivně projde celou strukturu a vytvoří
    seznam dvojic:

        (instance, path)
    """

    # 1. Přidání aktuálního uzlu
    nodes_list.append((instance, path))

    # 2. Zpracování konstanty (ukončení procesu)
    if instance.meta.is_constant:
        return

    # 3. Zpracování kompozice (cyklus skrze inners)
    for inner in instance.meta.inners:

        # 3.1 Vytvoření proměnné meta
        inner_meta = inner.meta

        # 3.2 Načtení instance
        inner_instance = getattr(
            instance,
            inner_meta.name_private
        )

        # 3.3 Rekurzní volání pro další vnoření
        _collect_nodes_data(
            instance=inner_instance,
            path=path + (inner_meta.name_snake,),
            nodes_list=nodes_list
        )