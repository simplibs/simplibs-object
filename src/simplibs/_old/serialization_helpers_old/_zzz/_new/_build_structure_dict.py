def _build_structure_dict(nodes_tuple) -> dict:
    """
    Sestaví referenční slovník struktury.
    Každý list uzel obsahuje odkaz na instanci a její validační metodu.
    Vnitřní uzly obsahují '_instance' a vnořené klíče.
    """
    result = {}
    for instance, path in nodes_tuple:

        if not path:
            result["_instance"] = instance
            continue

        current = result
        for key in path[:-1]:
            current = current.setdefault(key, {})
        current[path[-1]] = {
            "_instance": instance,
        }

    return result