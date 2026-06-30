from typing import TYPE_CHECKING
# Inners
from .PickleState import PickleState
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.lifecycles import PickleReduceProtocol
    from ....protocols.mixins.dunders.lifecycles.internal_types import PicklePlan


class PicleReduce(PickleState):
    """
    Poskytuje implementaci pickle protokolu (__reduce__).

    Logika:
    - Konstruktor = self.__class__
    - Argumenty = ()
    - Stav = self.__getstate__()

    DictPickle zajistí, že __getstate__/__setstate__ pracují přes to_dict/from_dict.

    Tento mixin dědí z DictPickle proto, aby měl k dispozici výchozí
    implementaci metody __getstate__, která využívá logiku SerializationBase
    a její metodu to_dict(). Pokud uživatel potřebuje, aby __getstate__
    pracoval jiným způsobem, může jej jednoduše přetížit vlastním mixinem,
    který se v MRO umístí nad tento mixin a tím původní implementaci nahradí.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - REDUCE
    # ----------------------------------------

    def __reduce__(
        self: "PickleReduceProtocol"
    ) -> "PicklePlan":
        """
        Pickle protokol:
        - callable: třída instance
        - args: žádné (třída si vytvoří instanci sama)
        - state: dict vrácený __getstate__

        Poznámka:
        - mutable instance vytvoří create_instance přes __class__()
        - immutable instance vytvoří snapshot-based instanci přes __setstate__
        """
        return (
            self.__class__,
            (),
            self.__getstate__()
        )
