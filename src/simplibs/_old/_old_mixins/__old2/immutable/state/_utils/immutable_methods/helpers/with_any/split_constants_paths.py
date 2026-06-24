from typing import Any


def split_constants_paths(
    constants: list[tuple[str, Any]],
    used_paths_dict: dict,
    nodes_path_dict: dict
) -> tuple[dict, dict]:
    """
    Rozdělí všechny konstantní cesty (paths) do dvou skupin:

    - contained: cesty, které leží uvnitř některé z uvedených cest
    - unique:    cesty, které nespadají pod žádnou root cestu

    Příklad:
        root_paths = {
            "A": (0,),
            "D": (3,)
        }

        paths = {
            "B": (0, 1),
            "C": (0, 1, 2),
            "E": (4,),
        }

        Výsledek:
            contained = {
                "B": (0,1),
                "C": (0,1,2)
            }

            unique = {
                "E": (4,)
            }

    Logika:
    - root_paths obsahuje jen nejvyšší (root) cesty
    - každou cestu z paths porovnáme s každým root
    - pokud cesta začíná root prefixem → patří do contained
    - jinak → patří do unique
    """

    # 1. Vtyoření proměných
    constants_paths = {name: nodes_path_dict[name] for name, _ in constants}
    used_paths = used_paths_dict.values()

    # 2. Vytvoření kontejnerů
    contained = {}
    unique = {}

    # 3. Roztřídění cest
    for key, path in constants_paths.items():

        # 3.1 Pokud path začíná některým root → patří do contained
        if any(
            path[:len(used_path)] == used_path
            for used_path in used_paths
        ):
            contained[key] = path

        # 3.2 Jinak → je to unikátní cesta mimo root větve
        else:
            unique[key] = path

    # 4. Vrátíme dvojici slovníků
    return contained, unique
