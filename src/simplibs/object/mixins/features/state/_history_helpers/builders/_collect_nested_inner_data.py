# noinspection PyProtectedMember
def _collect_nested_inner_data(instance, path, snapshot):
    """Rekurzivní funkce pro pžidání vnitřních prvků"""

    # 1. Procházení inners
    for inner in instance.meta.inners:

        # 2. Načtení proměných
        inner_meta = inner.meta
        name_private = inner_meta.name_private

        # 3. Vytvoření instance a cesty
        inner_instance = getattr(instance, name_private)
        new_path = path + (name_private,)

        # 4. Přidání záznamu
        snapshot.append((new_path, inner_instance._value))

        # 5. Vyřízení kompozic
        if not inner_meta.is_constant:
            _collect_nested_inner_data(inner_instance, new_path, snapshot)
