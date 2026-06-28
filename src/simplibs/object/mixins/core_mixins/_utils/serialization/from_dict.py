from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...._common.constants import OWNER_CLASS, VALUE
from ...._common.immutability import create_new_instance
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.core_mixins import SerializationProtocol
    from .....protocols.alias_typings import StateDict


def from_dict(
    self: "SerializationProtocol",
    user_dict: "StateDict"
) -> "SerializationProtocol":
    """
    Univerzální rekonstrukce stavu instance ze slovníku.
    Podporuje jak mutable (in-place zápis), tak immutable (generování nové instance) režim.
    """
    # 1. Validace vstupu
    if not isinstance(user_dict, dict):
        raise TypeError("Input must be a dictionary.")

    # 2. Validace owner class
    owner_class = user_dict.get(OWNER_CLASS, UNSET)
    if self.meta.owner_class != owner_class:
        raise ValueError(
            f"Owner class mismatch. Expected: {self.meta.owner_class}, Got: {owner_class}"
        )

    # 3. Příprava struktur pro traversal
    values = []
    last_composite_key = UNSET
    last_composite_dict = {}

    # 4. Načtení a validace hodnot z dictu podle stromu _nodes_tuple
    for instance, path in self._nodes_tuple:

        # 4.1 Definice proměnných
        current_dict = user_dict
        last_key = path[-1]

        # 4.2 Získání proměnných pokud se nejedná o root položky
        if len(path) > 1:

            # 4.2.1 Načtení předposledního klíče
            before_last_key = path[-2]

            # 4.2.2 Pokud se jedná o stejný slovník jako poslední
            if last_composite_key == before_last_key:
                current_dict = last_composite_dict

            # 4.2.3 Pokud se jedná o jiný slovník než poslední
            else:

                # 4.2.3.1 Traversal do správného pod-slovníku
                for key in path[:-1]:
                    current_dict = current_dict.get(key, UNSET)
                    if current_dict is UNSET:
                        raise KeyError(f"Missing key: {key}")
                    if not isinstance(current_dict, dict):
                        raise KeyError(f"Invalid structure at: {key}")

                # 4.2.3.2 Zápis posledního kompozitního slovníku
                if last_key == VALUE:
                    last_composite_key = before_last_key
                    last_composite_dict = current_dict

        # 4.3 Načtení hodnoty
        value = current_dict.get(last_key, UNSET)
        if value is UNSET:
            raise KeyError(f"Missing key: {last_key}")

        # 4.4 Validace a přidání hodnoty
        instance.validate(value)
        values.append(value)

    # 5. Vyřízení mutable -> Zápis hodnot
    if self.__is_mutable__:
        for (instance, _), value in zip(self._nodes_tuple, values):
            instance._value = value
        return self

    # 6. Vyřízení immutable -> Vytvoření nové instance ze snapshotu
    new_snapshot = tuple(values)
    return create_new_instance(self, new_snapshot)