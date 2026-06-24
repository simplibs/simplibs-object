from simplibs.sentinels import UNSET
# Outers
from ......protocols import SimpleInstanceType
from ....._constants import OWNER_CLASS, VALUE
from ..immutable_methods.helpers import create_new_instance


# noinspection PyProtectedMember
def from_dict(self: SimpleInstanceType, user_dict: dict) -> SimpleInstanceType:
    """
    1) Validuje OWNER_CLASS
    2) Načte hodnoty z dictu podle _nodes_tuple
    3) Validuje hodnoty
    4) Vytvoří nový snapshot
    5) Vrátí novou immutable instanci
    """
    if not isinstance(user_dict, dict):
        raise ...

    # 1. Validace owner class
    owner_class = user_dict.get(OWNER_CLASS, UNSET)
    if self.meta.owner_class is not owner_class:
        raise ValueError("Owner class mismatch")

    # 2. First pass – načtení hodnot v pořadí _nodes_tuple
    values = []
    last_composite_key = UNSET
    last_composite_dict = {}

    for instance, path in self._nodes_tuple:

        current_dict = user_dict
        last_key = path[-1]

        if len(path) > 1:
            before_last_key = path[-2]

            if last_composite_key == before_last_key:
                current_dict = last_composite_dict
            else:
                for key in path[:-1]:
                    current_dict = current_dict.get(key, UNSET)
                    if current_dict is UNSET:
                        raise KeyError(f"Missing key: {key}")
                    if not isinstance(current_dict, dict):
                        raise KeyError(f"Invalid structure at: {key}")

                if last_key == VALUE:
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        value = current_dict.get(last_key, UNSET)
        if value is UNSET:
            raise KeyError(f"Missing key: {last_key}")

        # Validace hodnoty
        instance.validate(value)
        values.append(value)

    # 3. Vytvoření snapshotu a nové instance
    new_snapshot = tuple(values)
    return create_new_instance(self, new_snapshot)