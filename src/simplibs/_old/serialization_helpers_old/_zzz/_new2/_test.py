from timeit import timeit


# ============================================================
# FAKE INSTANCE
# ============================================================

class FakeMeta:

    def __init__(self, is_constant):
        self.is_constant = is_constant


class FakeInstance:

    def __init__(self):
        self._value = None
        self.meta = FakeMeta(True)

    def validate(self, value):
        return True


# ============================================================
# TEST DATA GENERATOR
# ============================================================

def generate_structure(depth=5, branches=3):

    counter = 0

    def build(level):

        nonlocal counter

        if level >= depth:

            counter += 1

            return FakeInstance()

        return {
            f"k{i}": build(level + 1)
            for i in range(branches)
        }

    return build(0)


def generate_snapshot(structure):

    if isinstance(structure, FakeInstance):
        return 123

    return {
        key: generate_snapshot(value)
        for key, value in structure.items()
    }


# ============================================================
# NODES TUPLE
# ============================================================

def build_nodes_tuple(structure):

    result = []

    def walk(node, path):

        if isinstance(node, FakeInstance):
            result.append((node, path))
            return

        for key, value in node.items():
            walk(value, (*path, key))

    walk(structure, ())

    return tuple(result)


# ============================================================
# VARIANTA A
# ============================================================

def from_dict_fast(structure, received_dict):

    result = []

    def walk(received, default):

        if isinstance(received, dict):

            if not isinstance(default, dict):
                raise ValueError

            if received.keys() != default.keys():
                raise ValueError

            for key in received:
                walk(received[key], default[key])

        else:

            if isinstance(default, dict):
                raise ValueError

            default.validate(received)

            result.append((received, default))

    walk(received_dict, structure)

    for value, instance in result:
        instance._value = value


# ============================================================
# VARIANTA B
# ============================================================

def dict_to_nodes(snapshot):

    result = []

    def walk(node, path):

        if not isinstance(node, dict):
            result.append((path, node))
            return

        for key, value in node.items():
            walk(value, (*path, key))

    walk(snapshot, ())

    return tuple(result)


def from_dict_middle(nodes_tuple, received_dict):

    received_nodes = dict_to_nodes(received_dict)

    result = []

    for (instance, path), (received_path, value) in zip(
        nodes_tuple,
        received_nodes,
        strict=True,
    ):

        if path != received_path:
            raise ValueError

        instance.validate(value)

        result.append((value, instance))

    for value, instance in result:
        instance._value = value


# ============================================================
# VARIANTA C
# ============================================================

def get_by_path(data, path):

    try:
        current = data

        for key in path:
            current = current[key]

        return current
    except Exception:
        raise ...


def from_dict_slow(nodes_tuple, data):

    result = []

    for instance, path in nodes_tuple:

        value = get_by_path(data, path)


        instance.validate(value)

        result.append((instance, value))

    for instance, value in result:
        instance._value = value


# ============================================================
# BENCHMARK
# ============================================================

def benchmark(fn, loops=100):

    return timeit(fn, number=loops)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    DEPTH = 100
    BRANCHES = 1

    structure = generate_structure(
        depth=DEPTH,
        branches=BRANCHES,
    )

    snapshot = generate_snapshot(structure)

    nodes_tuple = build_nodes_tuple(structure)

    print(
        f"nodes: {len(nodes_tuple)}"
    )

    print()

    print(
        "FAST:",
        benchmark(
            lambda: from_dict_fast(
                structure,
                snapshot,
            )
        )
    )

    print(
        "MIDDLE:",
        benchmark(
            lambda: from_dict_middle(
                nodes_tuple,
                snapshot,
            )
        )
    )

    print(
        "SLOW:",
        benchmark(
            lambda: from_dict_slow(
                nodes_tuple,
                snapshot,
            )
        )
    )