def reverse_dict(d: dict) -> dict:
    return {
        key: reverse_dict(val) if isinstance(val, dict) else val
        for key, val in reversed(d.items())
    }

def snapshot_to_dict1(snapshot: tuple) -> dict:

    result = {}

    for path, value in reversed(snapshot):

        # 1. Odstranění prefixů
        clean_path = tuple(key.removeprefix("_") for key in path)

        # 2. Kořenový záznam
        if not clean_path:
            result["value"] = value
            continue

        # 3. Navigace ke správnému rodiči
        current = result
        for key in clean_path[:-1]:
            current = current.setdefault(key, {})

        # 4. Zápis hodnoty
        last_key = clean_path[-1]

        if last_key in current:
            # Kompozice — klíč už existuje (vytvořil ho potomek)
            current[last_key]["value"] = value
        else:
            # Konstanta — klíč ještě neexistuje
            current[last_key] = value

    return reverse_dict(result)

def snapshot_to_dict2(snapshot):

    result = {}

    parent_paths = {
        path[:i]
        for path, _ in snapshot
        for i in range(len(path))
    }

    for path, value in snapshot:

        if not path:
            result["value"] = value
            continue

        current = result

        for key in path[:-1]:

            key = key.removeprefix("_")

            current = current.setdefault(key, {})

        last_path = path
        last_key = path[-1].removeprefix("_")

        if last_path in parent_paths:
            current[last_key] = {"value": value}
        else:
            current[last_key] = value

    return result

def snapshot_to_dict3(snapshot):

    # Definice slovníku
    result = {}

    last_created_key = None

    # Cyklus na položky snapshotu
    for path, value in snapshot:

        # Vyřízení kořenové hodnotx
        if not path:
            result["value"] = value
            continue

        # Odstranění prefixů
        clean_path = tuple(key.removeprefix("_") for key in path)

        # Pokud je jen jeden prvek
        if len(clean_path) == 1:
            key = clean_path[0]
            result[key] = value
            last_created_key = key
            continue

        # Kontrola unikátnosti
        is_same_key = clean_path[-2] == last_created_key
        if is_same_key:

            previouse_key = clean_path[-2]
            new_key = clean_path[-1]

            current = result
            for key in clean_path[:-2]:
                current = current[key]
            last_value = current[previouse_key]

            current[previouse_key] = {
                "value": last_value,
                new_key: value
            }
            last_created_key = new_key
            continue

        else:

            new_key = clean_path[-1]

            current = result
            for key in clean_path[:-1]:
                current = current.setdefault(key, {})

            current[new_key] = value
            last_created_key = new_key


    return result


def generate_snapshot(depth: int, branches: int):

    result = [((), "root")]

    counter = 0

    for branch in range(branches):

        path = []

        for level in range(depth):

            counter += 1

            key = f"_k{counter}"

            path.append(key)

            result.append(
                (tuple(path), counter)
            )

    return tuple(result)


snapshot = generate_snapshot(
    depth=100,
    branches=100
)

from timeit import repeat


def benchmark(func, snapshot):

    result = min(
        repeat(
            lambda: func(snapshot),
            number=10,
            repeat=5
        )
    )

    return result


print(
    benchmark(snapshot_to_dict1, snapshot)
)

print(
    benchmark(snapshot_to_dict2, snapshot)
)

print(
    benchmark(snapshot_to_dict3, snapshot)
)