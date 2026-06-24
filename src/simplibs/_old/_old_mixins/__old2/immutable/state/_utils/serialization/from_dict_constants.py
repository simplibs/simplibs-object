from simplibs.sentinels import UNSET
# Outers
from ......protocols import SimpleInstanceType
from ....._constants import VALUE
from ..immutable_methods.helpers import create_new_instance
from ..immutable_methods import with_constants


# noinspection PyProtectedMember
def from_dict_constants(self: SimpleInstanceType, user_dict: dict) -> SimpleInstanceType:
    """
    Vrací novou instanci s aktualizovanými konstantami.
    Dict může být částečný – použijí se jen nalezené konstanty.
    """
    if not isinstance(user_dict, dict):
        raise ...

    changes: list[tuple[str, object]] = []

    # Cyklus procházející nodes tuple položky
    for instance, path in self._nodes_tuple:

        # Přeskočení kompozitních VALUE uzlů
        if path[-1] == VALUE:
            continue

        # Vyhledání hodnoty dle path
        current = user_dict
        for key in path:
            current = current.get(key, UNSET)
            if not isinstance(current, dict) and key != path[-1]:
                current = UNSET
                break

        # Pokud jsme našli konkrétní hodnotu (ne dict), bereme ji jako změnu
        if current is not UNSET:
            name = instance.meta.name_snake
            changes.append((name, current))

    if not changes:
        # Žádné změny → vracíme stejnou instanci
        return self

    # Delegace na immutable pipeline
    return with_constants(self, tuple(changes))