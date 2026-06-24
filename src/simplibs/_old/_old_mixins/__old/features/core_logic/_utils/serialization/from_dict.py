from simplibs.sentinels import UNSET
# Outers
from ....._constants import OWNER_CLASS, VALUE


# noinspection PyProtectedMember
def from_dict(self, user_dict: dict):

    # =========================================================
    # 1. VALIDACE OWNER CLASS
    # =========================================================
    owner_class = user_dict.get(OWNER_CLASS, UNSET)
    if self.meta.owner_class != owner_class:
        raise ValueError("Owner class mismatch")

    # =========================================================
    # 2. FIRST PASS (collect values only)
    # =========================================================
    values = []
    last_composite_key = UNSET
    last_composite_dict = {}

    for instance, path in self._nodes_tuple:

        # 2.1 Definice proměnných
        current_dict = user_dict
        last_key = path[-1]

        # 2.2 Získání proměnných pokud se nejedná o root položky
        if len(path) > 1:

            # 2.2.1 Načtení předposledního klíče
            before_last_key = path[-2]

            # 2.2.2 Pokud se jedná o stejný slovník jako poslední
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 2.2.3 Pokud se jedná o jiný slovník než poslední
            else:

                # 2.2.3.1 Traversal do správného pod-slovníku
                for key in path[:-1]:
                    current_dict = current_dict.get(key, UNSET)
                    if current_dict is UNSET:
                        raise KeyError(f"Missing key: {key}")
                    if not isinstance(current_dict, dict):
                        raise KeyError(f"Invalid structure at: {key}")

                # 2.2.3.2 Zápis posledního kompozitního slovníku
                if last_key == VALUE:
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        # 2.3 Načtení hodnoty
        value = current_dict.get(last_key, UNSET)
        if value is UNSET:
            raise KeyError(f"Missing key: {last_key}")
        values.append(value)

    # =========================================================
    # 3. SECOND PASS (apply values)
    # =========================================================
    for (instance, _), value in zip(self._nodes_tuple, values):
        instance.validate(value)
        instance._value = value