def _to_dict(nodes_tuple) -> dict:
    """Sestaví dict hodnot z nodes_tuple."""

    result = {}

    for instance, path in nodes_tuple:

        if not path:
            result["_value"] = instance._value
            continue

        current = result
        for key in path[:-1]:
            current = current.setdefault(key, {})
        current[path[-1]] = instance._value

    return result