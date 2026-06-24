from simplibs.sentinels import UNSET
# Outers
from ....._constants import OWNER_CLASS, VALUE


# noinspection PyProtectedMember
def to_dict(self, constant_only: bool = False):

    # 1. Definice proměných
    result = {OWNER_CLASS: self.meta.owner_class}
    last_composite_key = UNSET
    last_composite_dict = {}

    # 2. Cyklus dle pořadí nodes tuple
    for instance, path in self._nodes_tuple:

        # 2.1 Definice proměných
        value = instance._value
        current_dict = result
        last_key = path[0]

        # 2.2 Získání proměných pokud se nejedná o root položky
        if len(path) > 1:

            # 2.2.1 Načtení posledního a předposledního klíče
            last_key = path[-1]
            before_last_key = path[-2]

            # 2.2.2 Pokud se jedná o stejná slovník jako poslední
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 2.2.3 Pokud se jedná o jiný slovník než poslední
            else:

                # 2.2.3.1 Vytvoření nového pole
                for key in path[:-1]:
                    current_dict = current_dict.setdefault(key, {})

                # 2.2.3.2 Zápis posledního kompozitního slovníku
                if last_key == VALUE:
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        # 2.3 Zápis hodnoty
        if not (constant_only and last_key == VALUE):
            current_dict[last_key] = value

    # 3. Navrácení hotového slovníku
    return result

