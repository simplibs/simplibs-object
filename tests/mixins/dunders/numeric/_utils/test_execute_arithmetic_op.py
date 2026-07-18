from typing import TYPE_CHECKING, Any
# Outers
from ...._common.immutability import with_composite
# Inners
from ._align_operand_type import _align_operand_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.dunders.numeric import ArithmeticProtocol
    from .....protocols.mixins.dunders.numeric.internal_types import Operator


def execute_arithmetic_op(
    self: "ArithmeticProtocol",
    operator: "Operator",
    other: Any,
    *,
    is_reversed: bool = False
) -> Any:
    """Modulární exekutor pro standardní i pravostranné aritmetické operace."""

    # 1. Získání druhé hodnoty
    other_value = getattr(other, "value", other)

    # 2. Pokus o standardní výpočet a vytvoření nové instance
    try:
        value = (
            operator(other_value, self.value)
            if is_reversed
            else operator(self.value, other_value)
        )
        return with_composite(self, self.meta.name_snake, value)

    # 3. Pokus o přetypování při neúspěchu
    except TypeError:

        # 3.1 Přetypování
        coerced = _align_operand_type(self, other_value)

        # 3.2 Pokus o nový výpočet s přetypovanou hodnotou
        try:
            value = (
                operator(coerced, self.value)
                if is_reversed
                else operator(self.value, coerced)
            )
            return with_composite(self, self.meta.name_snake, value)

        # 3.3 Vyvolání výjimky při neúspěchu
        except TypeError:
            return NotImplemented