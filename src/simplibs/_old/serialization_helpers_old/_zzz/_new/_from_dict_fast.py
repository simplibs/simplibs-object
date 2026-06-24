def _from_dict_fast(instance, data: dict) -> None:
    """
    Rychlá cesta — předpokládá že data pochází z to_dict() stejné třídy.
    Prochází structure_dict a data paralelně, validuje a zapisuje.
    """
    values = []
    _collect_values_fast(instance._structure_dict, data, values)
    for (node_instance, _), value in zip(
        ((n, p) for n, p in instance._nodes_tuple if n.meta.is_constant),
        values
    ):
        node_instance.meta.owner_class.validate(value)
        object.__setattr__(node_instance, "_value", value)
    _recalculate_composites(instance)


def _collect_values_fast(structure, data, values) -> None:
    """Rekurzivně projde structure_dict a data paralelně."""
    for key, struct_node in structure.items():
        if key == "_instance":
            continue
        if key not in data:
            raise SimpleLogicError(
                f"Chybí klíč '{key}' v předaném dict."
            )
        if isinstance(struct_node, dict):
            node_instance = struct_node.get("_instance")
            if node_instance and node_instance.meta.is_constant:
                values.append(data[key])
            else:
                _collect_values_fast(struct_node, data[key], values)
        else:
            values.append(data[key])