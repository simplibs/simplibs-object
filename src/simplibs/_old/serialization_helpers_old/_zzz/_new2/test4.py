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
# GENERATOR – REALISTIC COMPOSITE MODEL
# ============================================================

def generate_realistic_nodes(depth=5):

    nodes = []
    counter = 0

    def build(path, level):

        nonlocal counter

        # ----------------------------------------------------
        # každá kompozice má svoji hodnotu
        # ----------------------------------------------------
        comp = FakeInstance(counter)
        counter += 1

        nodes.append(
            (comp, path + (VALUE,))
        )

        # ----------------------------------------------------
        # 2 konstanty (typicky metadata / hodnoty)
        # ----------------------------------------------------
        for i in range(2):

            leaf = FakeInstance(counter)
            counter += 1

            nodes.append(
                (leaf, path + (f"c{i}_{counter}",))
            )

        # ----------------------------------------------------
        # další kompozice (1 větev)
        # ----------------------------------------------------
        if level < depth:

            counter += 1
            inner_key = f"inner_{counter}"

            build(
                path + (inner_key,),
                level + 1
            )

    build((), 0)

    return tuple(nodes)


# ============================================================
# SIMPLE VERSION
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
# CACHED VERSION
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


def to_dict_cached_fast(nodes_tuple):

    result = {}

    last_parent_path = None
    last_parent_dict = None

    for instance, path in nodes_tuple:

        value = instance._value

        if len(path) == 1:
            result[path[0]] = value
            continue

        parent_path = path[:-1]
        last_key = path[-1]

        # ================================
        # FAST PATH (reuse dictionary)
        # ================================
        if parent_path == last_parent_path:

            last_parent_dict[last_key] = value
            continue

        # ================================
        # SLOW PATH (build dictionary path)
        # ================================
        current = result

        for key in parent_path:
            current = current.setdefault(key, {})

        current[last_key] = value

        # cache update
        last_parent_path = parent_path
        last_parent_dict = current

    return result


# ============================================================
# BENCHMARK
# ============================================================

def bench(fn, loops=500):

    return timeit(fn, number=loops)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500):

        nodes_tuple = generate_realistic_nodes(i)
        print("DEPTH = ", i)
        print("nodes:", len(nodes_tuple))
        print("simple:", bench(lambda: to_dict_simple(nodes_tuple)))
        print("cached:", bench(lambda: to_dict_cached(nodes_tuple)))
        print("fast:", bench(lambda: to_dict_cached_fast(nodes_tuple)))
        print()