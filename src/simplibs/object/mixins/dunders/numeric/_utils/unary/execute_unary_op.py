# Outers
from .....immutable._utils.immutable_methods.with_composite import with_composite
from ..common import align_operand_type


def execute_unary_op(self, op):
    """
    Rychlý modulární exekutor pro unární numerické operace.
    Aplikuje operátor na self.value a vrací novou instanci přes with_composite.
    Obsahuje fallback pro bezpečné zarovnání typu.
    """

    # 1. Pokus o standardní výpočet
    try:
        return with_composite(self, self.meta.name_snake, op(self.value))

    # 2. Pokus o přetypování
    except TypeError:

        # 2.1 Přetypování
        coerced = align_operand_type(self, self.value)

        # 2.2 Pokus o nový výpočet
        try:
            return with_composite(self, self.meta.name_snake, op(coerced))

        # 2.3 Vyvolání výjimky při neúspěchu
        except TypeError:
            return NotImplemented