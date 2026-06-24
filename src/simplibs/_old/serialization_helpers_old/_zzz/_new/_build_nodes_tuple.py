def _build_nodes_tuple(instance) -> tuple:
    nodes = []
    _collect_nodes(instance, (), nodes)
    return tuple(nodes)


def _collect_nodes(instance, path, nodes):

    nodes.append((instance, path))

    if instance.meta.is_constant:
        return

    for inner in instance.meta.inners:

        inner_meta = inner.meta

        inner_instance = getattr(instance, inner_meta.name_private)

        _collect_nodes(inner_instance, path + (inner_meta.name_snake,), nodes)


nodes_tuple = tuple(_collect_nodes(instance, (), []))