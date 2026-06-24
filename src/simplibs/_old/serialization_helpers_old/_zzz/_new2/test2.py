from timeit import timeit


VALUE = "_value"


# ============================================================
# FAKE INSTANCE
# ============================================================

class FakeInstance:

    __slots__ = ("_value",)

    def __init__(self, value):
        self._value = value


# ============================================================
# GENERATOR
# ============================================================

def generate_nodes_tuple(depth=5, branches=3):

    nodes = []

    counter = 0

    def build(path, level):

        nonlocal counter

        # ----------------------------------------------------
        # kompozice
        # ----------------------------------------------------

        composite = FakeInstance(counter)
        counter += 1

        nodes.append(
            (
                composite,
                path + (VALUE,)
            )
        )

        # ----------------------------------------------------
        # list
        # ----------------------------------------------------

        if level >= depth:

            leaf = FakeInstance(counter)
            counter += 1

            nodes.append(
                (
                    leaf,
                    path + (f"leaf_{counter}",)
                )
            )

            return

        # ----------------------------------------------------
        # inners
        # ----------------------------------------------------

        for i in range(branches):

            counter += 1

            key = f"node_{counter}"

            build(
                path + (key,),
                level + 1
            )

    build((), 0)

    return tuple(nodes)


# ============================================================
# SIMPLE
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
# OPTIMIZED
# ============================================================

UNSET = None


def to_dict_cached(nodes_tuple):

    result = {}

    last_composite_key = UNSET
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
# BENCH
# ============================================================

def bench(fn, loops=100):

    return timeit(fn, number=loops)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    DEPTH = 100
    BRANCHES = 1

    nodes_tuple = generate_nodes_tuple(
        depth=DEPTH,
        branches=BRANCHES
    )

    print(
        "nodes:",
        len(nodes_tuple)
    )

    print()

    print(
        "simple:",
        bench(
            lambda: to_dict_simple(nodes_tuple)
        )
    )

    print(
        "cached:",
        bench(
            lambda: to_dict_cached(nodes_tuple)
        )
    )