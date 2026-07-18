from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Outers
from ...._common.constants import VALUE
from ...._common.immutability import with_constants
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.core_mixins import SerializationProtocol
    from .....protocols.alias_typings import StateDict


def from_dict_constants(
    self: "SerializationProtocol",
    user_dict: "StateDict"
) -> "SerializationProtocol":
    """
    Aktualizuje konstanty (atomy) objektu z částečného nebo úplného slovníku.

    Automaticky detekuje režim objektu:
    - V mutable režimu: Mění hodnoty konstant přímo na místě (in-place).
    - V immutable režimu: Vrací novou instanci s aplikovanými změnami.
    """

    # 1. Validace slovníku
    if not isinstance(user_dict, dict):
        raise TypeError("Input must be a dictionary.")

    # 2. Definice seznamu pro zběr změn pro immutable verzy
    changes: list[tuple[str, object]] = []

    # 3. Procházení všech uzlů a vyhledávání hodnot podle cest (path)
    for instance, path in self._nodes_tuple:

        # 3.1 Přeskočení kompozitních VALUE uzlů (zajímají nás jen čisté konstanty)
        if path[-1] == VALUE:
            continue

        # 3.2 Vyhledání hodnoty hluboko ve struktuře předaného slovníku
        current = user_dict
        for key in path:
            current = current.get(key, UNSET)
            if not isinstance(current, dict) and key != path[-1]:
                current = UNSET
                break

        # 3.3 Pokud byla hodnota nalezena -> rozcestník podle mutability
        if current is not UNSET:

            # 3.3.1 MUTABLE REŽIM -> Zápis rovnou na místě (in-place)
            if self.__is_mutable__:
                instance.value = current

            # 3.3.2 IMMUTABLE REŽIM -> Sběr změn pro hromadný update
            else:
                name = instance.meta.name_snake
                changes.append((name, current))

    # 4. Vyřízení pro mutable (a pro immutable pokud nejsou změny)
    if self.__is_mutable__ or not changes:
        return self

    # 5. Vyřízení immutable při změnách
    return with_constants(self, tuple(changes))