from typing import TYPE_CHECKING, Any
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.comparison import EqualityProtocol


class Equality(SimpleMixin):
    """
    Rovnost a hashování pro Simple instance.

    Rovnost (__eq__) je založená na hodnotě:
    - Pokud je druhý operand Simple instance stejného blueprintu,
      porovnají se jejich hodnoty.
    - Pokud je druhý operand surová hodnota, porovnává se přímo s ní.

    Hashování (__hash__) je řízené mutabilitou instance:
    - U mutovatelných instancí (__is_mutable__ = True) se používá
      hash podle identity (id(self)), aby byla zaručena stabilita
      i při změně hodnoty.
    - U neměnných instancí (__is_mutable__ = False) se používá
      hash podle hodnoty (hash(self.value)), protože hodnota je
      garantovaně neměnná a hashovatelná.

    Tento mixin je univerzální — lze jej použít pro mutable i immutable
    instance, protože hashovací strategie se volí dynamicky podle
    příznaku __is_mutable__.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - EQ / HASH
    # ----------------------------------------

    def __eq__(
        self: "EqualityProtocol",
        other: Any
    ) -> bool:
        """
        Rovnost podle hodnoty.
        - Pokud je druhý operand Simple instance stejného blueprintu,
          porovnají se jejich hodnoty.
        - Pokud je druhý operand surová hodnota, porovná se přímo.
        """
        # 1. Porovnání dvou Simple instancí
        if hasattr(other, "meta") and hasattr(other, "value"):
            if self.meta.blueprint_path == other.meta.blueprint_path:
                return self.value == other.value
            return False

        # 2. Porovnání s přímou hodnotou
        return self.value == other

    def __hash__(
        self: "EqualityProtocol"
    ) -> int:
       """
       Vrací hash podle mutability instance.

       - U mutovatelných instancí (__is_mutable__ = True) vrací hash založený
         na identitě objektu (id(self)), aby byla zaručena stabilita i při
         změně hodnoty.

       - U neměnných instancí (__is_mutable__ = False) vrací hash hodnoty
         (hash(self.value)), protože hodnota je garantovaně neměnná a
         hashovatelná.

       Tato metoda tak sjednocuje hashování pro mutable i immutable režim
       v rámci jednoho mixinu.
       """
       return (
           id(self)
           if self.__is_mutable__ else
           hash(self.value)
       )