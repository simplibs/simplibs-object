UNSET = None
VALUE = "_value"
OWNER_CLASS = "_owner_class"


# noinspection PyProtectedMember
def to_dict(self, constant_only: bool = False):

    # 1. Definice proměných
    result = {OWNER_CLASS: self.meta.owner_class}
    last_composite_key = UNSET
    last_composite_dict = {}

    # 2. Cyklus dle pořadí nodes tuple
    for instance, path in self._nodes_tuple:

        # 2.1 Načtení hodnoty z instance
        value = instance._value

        # 2.2 Vyřízení pro jeden prvek
        if len(path) == 1:
            if not (constant_only and path[0] == VALUE):
                result[path[0]] = value
            continue

        # 2.3 Načtení posledního a předposledního klíče
        last_key = path[-1]

        # 2.4 Zápis do stejného kompozitního slovníku
        if last_composite_key == path[-2]:
            last_composite_dict[last_key] = value
            continue

        # 2.5 Vytvoření nového pole
        current = result
        for key in path[:-1]:
            current = current.setdefault(key, {})

        if not (constant_only and last_key == VALUE):
            current[last_key] = value

        # 2.6 Kontrola zda se jedná o kompozici
        if last_key == VALUE:
            last_composite_key = path[-2]
            last_composite_dict = current

    # 3. Navrácení hotového slovníku
    return result

