from typing import TYPE_CHECKING, Any
# Outers
from ...._common.immutability import with_composite
# Inners
from ._align_operand_type import _align_operand_type
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.dunders.numeric import UnaryProtocol
    from .....protocols.mixins.dunders.numeric.internal_types import UnaryOperator


def execute_unary_op(
    self: "UnaryProtocol",
    operator: "UnaryOperator"
) -> Any:
    """
    Rychlý modulární exekutor pro unární numerické operace.
    Aplikuje operátor na self.value a vrací novou instanci přes with_composite.
    Obsahuje fallback pro bezpečné zarovnání typu.
    """

    # 1. Pokus o standardní výpočet
    try:
        return with_composite(self, self.meta.name_snake, operator(self.value))

    # 2. Pokus o přetypování
    except TypeError:

        # 2.1 Přetypování
        coerced = _align_operand_type(self, self.value)

        # 2.2 Pokus o nový výpočet
        try:
            return with_composite(self, self.meta.name_snake, operator(coerced))

        # 2.3 Vyvolání výjimky při neúspěchu
        except TypeError:
            return NotImplemented