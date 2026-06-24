UNSET = None
VALUE = "_value"


# noinspection PyProtectedMember
def to_dict(self, constants_only: bool = False):

    # 1. Definice proměných
    result = {}
    last_composite_key = UNSET
    last_composite_dict = {}

    # 2. Cyklus dle pořadí nodes tuple
    for instance, path in self._nodes_tuple:

        # 2.1 Načtení hodnoty z instance
        value = instance._value

        # 2.2 Vyřízení pro jeden prvek
        if len(path) == 1:
            result[path[0]] = value
            continue

        # 2.3 Načtení posledního a předposledního klíče
        last_key = path[-1]

        # 2.4 Zápis do stejného kompozitního slovníku
        if last_composite_key == path[-2]:
            last_composite_dict[last_key] = value

        # 2.5 Vytvoření nového pole
        else:
            current = result
            for key in path[:-1]:
                current = current.setdefault(key, {})
            current[last_key] = value

            # 2.6 Kontrola zda se jedná o kompozici
            if last_key == VALUE:
                last_composite_key = path[-2]
                last_composite_dict = current

    # 3. Navrácení hotového slovníku
    return result

