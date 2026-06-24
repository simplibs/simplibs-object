from typing import Any


def get_top_composite_paths(
    composite: list[tuple[str, Any]],
    nodes_path_dict: dict
) -> tuple[dict, dict]:
    """
    Vrátí pouze ty cesty, které jsou nejblíže kořeni — tedy takové,
    které nejsou podcestou žádné jiné cesty v tomto slovníku.

    Příklad:
        paths = {
            "a": (0,),
            "b": (0, 1),
            "c": (0, 1, 2),
            "d": (3,)
        }

        Výsledek:
            {
                "a": (0,),   # protože (0,) je prefix (0,1) i (0,1,2)
                "d": (3,)    # protože (3,) není prefix žádné jiné cesty
            }

    Logika:
    - Seřadíme cesty podle délky (kratší = výše v hierarchii)
    - Pro každou cestu ověříme, zda není prefixem některé již uložené root cesty
    - Pokud není prefixem žádné existující root cesty → je to nový root
    """

    # 1. Vytvoření proměnných
    top_composite = {}
    top_composite_paths = []
    child_composite = {}

    # 2. Vytvoření seřazeného slovníku cest
    composite_names = (name for name, _ in composite)
    sorted_paths = sorted(
        ((name, nodes_path_dict[name]) for name in composite_names),
        key=lambda item: len(item[1])
    )

    # 3. Filtrace kořenových cest
    for key, path in sorted_paths:

        # 3.1 Zpracování top kompozic
        if not any(
            path[:len(parent)] == parent
            for parent in top_composite_paths
        ):
            top_composite[key] = path
            top_composite_paths.append(path)

        # 3.2 Zpracování vnitřních kompozic
        else:
            child_composite[key] = path

    # 4. Návrat obou slovníků
    return top_composite, child_composite

