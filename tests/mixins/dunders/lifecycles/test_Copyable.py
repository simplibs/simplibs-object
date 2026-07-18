from typing import Any, TYPE_CHECKING
import copy as _copy
# Outers
from ...core_mixins import NodesDicts, Snapshot
from ..._common.immutability import create_new_instance
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.lifecycles import CopyableProtocol


class Copyable(NodesDicts, Snapshot):
    """
    Společný mixin pro mutable a immutbale verzy.

    Mutable lifecycle:
    - mělká kopie přes create_instance(validate=False)
    - hluboká kopie přes create_instance(validate=False)

    Immutable lifecycle:
    - mělká kopie přes snapshot
    - hluboká kopie přes deepcopy snapshotu
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - COPY / DEEPCOPY
    # ----------------------------------------

    def __copy__(
        self: "CopyableProtocol"
    ) -> "CopyableProtocol":
        """
        Vytvoří a vrátí mělkou kopii (shallow copy) této instance.
        Bezpečně reaguje na mutable/immutable režim objektu.
        """

        # 1. Vytvoření snapshotu
        snapshot = self._build_snapshot()

        # 2. Vytvoření a vrácení nové instace
        return create_new_instance(self, snapshot)

    def __deepcopy__(
        self: "CopyableProtocol",
        memo: dict[int, Any]
    ) -> "CopyableProtocol":
        """
        Vytvoří a vrátí hlubokou kopii (deep copy) této instance.
        Slovník `memo` slouží k internímu sledování již navštívených
        objektů kvůli zamezení zacyklení.
        """

        # 1. Vytvoření snapshotu
        snapshot = tuple(
            _copy.deepcopy(v, memo)
            for v in self._build_snapshot()
        )

        # 2. Vytvoření a vrácení nové instace
        return create_new_instance(self, snapshot)
