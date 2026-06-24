from ._collect_nodes_data import _collect_nodes_data


def build_nodes_tuple(instance):
    """
    Vytvoří tuple:
        (
            (instance, path),
            ...
        )

    kde path obsahuje name_snake názvy vedoucí k danému uzlu.
    """

    nodes_list = []

    _collect_nodes_data(
        instance=instance,
        path=(),
        nodes_list=nodes_list
    )

    return tuple(nodes_list)