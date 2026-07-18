from typing import TYPE_CHECKING, Any
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.comparison import OrderingProtocol


# noinspection PyUnresolvedReferences
class Ordering(SimpleMixin):
    """
    Porovnávání velikosti pro Simple instance.
    Porovnává podle hodnoty (self.value).
    Funguje pro porovnání instance s instancí i s přímou hodnotou.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - LT / LE / GT / GE
    # ----------------------------------------

    def __lt__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Vrací True, pokud je hodnota této instance menší než hodnota druhého
        operandu. Pokud je operand Simple instance, použije se jeho .value,
        jinak se porovnává přímo s hodnotou operandu. Při nekompatibilních
        typech vrací NotImplemented.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value < other_value
        except TypeError:
            return NotImplemented

    def __le__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Vrací True, pokud je hodnota této instance menší nebo rovna hodnotě
        druhého operandu. Pokud je operand Simple instance, použije se jeho
        .value, jinak se porovnává přímo s hodnotou operandu. Při
        nekompatibilních typech vrací NotImplemented.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value <= other_value
        except TypeError:
            return NotImplemented

    def __gt__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Vrací True, pokud je hodnota této instance větší než hodnota druhého
        operandu. Pokud je operand Simple instance, použije se jeho .value,
        jinak se porovnává přímo s hodnotou operandu. Při nekompatibilních
        typech vrací NotImplemented.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value > other_value
        except TypeError:
            return NotImplemented

    def __ge__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Vrací True, pokud je hodnota této instance větší nebo rovna hodnotě
        druhého operandu. Pokud je operand Simple instance, použije se jeho
        .value, jinak se porovnává přímo s hodnotou operandu. Při
        nekompatibilních typech vrací NotImplemented.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value >= other_value
        except TypeError:
            return NotImplemented
