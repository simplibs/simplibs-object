def _from_dict_slow(instance, data: dict) -> None:
    """
    Pomalá cesta — data mohou mít libovolný původ.
    Prochází nodes_tuple a pro každý uzel hledá hodnotu v data podle path.
    """

    values = []

    for node_instance, path in instance._nodes_tuple:

        if not node_instance.meta.is_constant:
            continue

        value = _get_by_path(data, path)

        node_instance.validate(value)
        values.append((node_instance, value))

    for node_instance, value in values:
        # object.__setattr__(node_instance, "_value", value)
        node_instance._value = value

    _log_this()


def _get_by_path(data: dict, path: tuple):
    """Vytáhne hodnotu ze zanořeného dict podle path."""
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise SimpleLogicError(
                f"Klíč '{key}' nenalezen v předaném dict."
            )
        current = current[key]
    return current


# def _recalculate_composites(instance) -> None:
#     """Po zápisu hodnot přepočítá všechny kompozice zdola nahoru."""
#     for node_instance, _ in reversed(instance._nodes_tuple):
#         if not node_instance.meta.is_constant:
#             node_instance._recalculate_self()