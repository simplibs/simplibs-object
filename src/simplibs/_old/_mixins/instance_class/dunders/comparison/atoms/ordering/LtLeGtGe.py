from functools import total_ordering
from typing import Any
from .Eg import EqMixin


@total_ordering
class LtLeGtGeMixin(EqMixin):
    """
    Mixin umožňující porovnávání objektů (bohaté operátory <, >, <=, >=).
    Předpokládá, že IdentityMixin již řeší rovnost (==).
    """
    __slots__ = ()
    value: Any

    def __lt__(self, other: Any) -> bool:
        """
        Logika pro 'menší než' (<). 
        Umožňuje porovnání s jiným SimpleObjectem i s holou hodnotou.
        """
        # 1. Získáme hodnotu pro porovnání
        # Pokud má 'other' atribut 'value', použijeme ho, jinak bereme 'other' přímo.
        other_value = getattr(other, "value", other)

        # 2. Samotné porovnání s ošetřením nekompatibilních typů
        try:
            return self.value < other_value
        except TypeError:
            # Pokud Python neví, jak tyto dva typy porovnat, 
            # vrátíme NotImplemented, což umožní druhé straně zkusit porovnání.
            return NotImplemented

    # Metody __le__, __gt__, __ge__ doplní @total_ordering automaticky 
    # na základě __lt__ a tvého __eq__ z IdentityMixin.