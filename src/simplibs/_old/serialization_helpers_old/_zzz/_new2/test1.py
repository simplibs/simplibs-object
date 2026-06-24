from timeit import timeit


# ============================================================
# TEST DATA
# ============================================================

VALUE = "_value"


class FakeInstance:

    __slots__ = ("_value",)

    def __init__(self, value):
        self._value = value


def build_nodes_tuple(depth=5, branches=3):

    nodes = []

    counter = 0

    def walk(level, path):

        nonlocal counter

        # kompozice
        composite = FakeInstance(counter)
        counter += 1

        nodes.append(
            (composite, path + (VALUE,))
        )

        # list
        if level >= depth:
            return

        # děti
        for i in range(branches):

            counter += 1

            unique_name = f"n{counter}"

            child_path = path + (unique_name,)

            if level + 1 == depth:

                nodes.append(
                    (
                        FakeInstance(counter),
                        child_path
                    )
                )

            else:

                walk(
                    level + 1,
                    child_path
                )

    walk(0, ())

    return tuple(nodes)


# ============================================================
# VARIANTA A
# ============================================================

def to_dict_cached(nodes_tuple):

    result = {}

    last_composite_key = None
    last_composite_dict = {}

    for instance, path in nodes_tuple:

        value = instance._value

        if len(path) == 1:
            result[path[0]] = value
            continue

        last_key = path[-1]

        if last_composite_key == path[-2]:

            last_composite_dict[last_key] = value

        else:

            current = result

            for key in path[:-1]:
                current = current.setdefault(key, {})

            current[last_key] = value

            if last_key == VALUE:
                last_composite_key = path[-2]
                last_composite_dict = current

    return result


# ============================================================
# VARIANTA B
# ============================================================

def to_dict_simple(nodes_tuple):

    result = {}

    for instance, path in nodes_tuple:

        current = result

        for key in path[:-1]:
            current = current.setdefault(key, {})

        current[path[-1]] = instance._value

    return result


# ============================================================
# BENCHMARK
# ============================================================

def benchmark(fn, loops=1000):

    return timeit(
        fn,
        number=loops
    )


if __name__ == "__main__":
    DEPTH = 100
    BRANCHES = 1

    nodes_tuple = build_nodes_tuple(
        depth=DEPTH,
        branches=BRANCHES
    )

    print(
        "nodes:",
        len(nodes_tuple)
    )

    print()

    print(
        "cached:",
        benchmark(
            lambda: to_dict_cached(nodes_tuple)
        )
    )

    print(
        "simple:",
        benchmark(
            lambda: to_dict_simple(nodes_tuple)
        )
    )