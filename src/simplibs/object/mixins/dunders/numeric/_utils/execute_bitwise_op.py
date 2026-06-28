from typing import TYPE_CHECKING, Any
# Outers
from ...._common.immutability import with_constant
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.dunders.numeric import BitwiseProtocol
    from .....protocols.mixins.dunders.numeric.internal_types import Operator


def execute_bitwise_op(
    self: "BitwiseProtocol",
    operator: "Operator",
    other: Any,
    is_reversed: bool = False
) -> Any:
    """Modulární exekutor pro standardní i pravostranné bitové operace."""

    # 1. Získání druhé hodnoty
    other_value = getattr(other, "value", other)

    # 2. Pokus o výpočet se správným pořadím operandů
    try:
        value = (
            operator(other_value, self.value)
            if is_reversed
            else operator(self.value, other_value)
        )
        return with_constant(self, self.meta.name_snake, value)

    # 3. Vyvolání výjimky při neúspěchu
    except TypeError:
        return NotImplemented