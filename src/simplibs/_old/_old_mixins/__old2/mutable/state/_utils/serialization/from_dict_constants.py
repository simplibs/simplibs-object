from simplibs.sentinels import UNSET
# Outers
from ....._constants import VALUE


# noinspection PyProtectedMember
def from_dict_constants(self, user_dict: dict):

    if not isinstance(user_dict, dict):
        raise ...

    for instance, path in self._nodes_tuple:

        # Přeskočení kompozitních hodnot
        if path[-1] == VALUE:
            continue

        # Vyhledání hodnoty dle path
        current = user_dict
        for key in path:
            current = current.get(key, UNSET)
            if not isinstance(current, dict) and key != path[-1]:
                current = UNSET
                break

        # Zápis pokud byla hodnota nalezena
        if current is not UNSET:
            instance.value = current