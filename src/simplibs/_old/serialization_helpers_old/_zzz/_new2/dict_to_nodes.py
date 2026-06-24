def dict_to_nodes(snapshot) -> tuple:

    nodes = []

    def walk(node, path):

        if not isinstance(node, dict):
            nodes.append((path, node))
            return

        for key, value in node.items():

            if key == "_value":
                nodes.append((path, value))
            else:
                walk(value, (*path, key))

    walk(snapshot, ())

    return tuple(nodes)

def from_dict_midle(self, resived_dict):
    resived_dict_nodes = dict_to_nodes(resived_dict)

    default_nodes = self._nodes_tuple

    result = []

    for instance, path, value, resive_path in zip(default_nodes, resived_dict_nodes):
        if path != resive_path:
            raise ...
        instace.validate(value)
        result.append(value, instance)

    for value, instance in result:
        # object.__setattr__(instance, "_value", value)
        instance._value = value

    _log_this()