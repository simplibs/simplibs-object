# Outers
from ........protocols import SimpleClassType


def get_collision_path(
    current_class: SimpleClassType,
    collision_name: str,
) -> str | None:
    """
    Rekurzivně dohledá cestu k třídě, která způsobuje kolizi jména.

    Vrací řetězec ve formátu 'ClassA/ClassB/ClassC', kde ClassC je
    skutečným vlastníkem kolizního jména 'collision_name'.
    """

    # 1. Kontrola, zda je kolize přímo u této třídy
    # (Předpokládáme, že name_snake je unikátní identifikátor v rámci metadat)
    if current_class.meta.name_snake == collision_name:
        return current_class.__name__

    # 2. Pokud třída není přímým viníkem, musíme prohledat její vnitřní prvky (inners)
    # Přistupujeme k raw_inners (předpokládáme, že už jsou v meta nebo v __dict__)
    # Využíváme node_names_set pro rychlou kontrolu, zda má smysl do této větve lézt
    raw_inners = getattr(current_class, "_inners", ())

    for inner in raw_inners:
        # Pokud toto jméno existuje v množině použitých jmen tohoto potomka (nebo jeho dětí)
        if collision_name in inner.meta.node_names_set:
            # Rekurzivní ponor
            sub_path = get_collision_path(inner, collision_name)

            if sub_path:
                # Sestavení cesty: Aktuální jméno + to, co našla rekurze
                return f"{current_class.__name__}/{sub_path}"

    return None