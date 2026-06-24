# Outers
from .....immutable._utils.immutable_methods import with_composite
from ..common import align_operand_type



def execute_op(self, op, other):
    """Rychlý modulární exekutor pro standardní operace (self.value op other_value)."""

    # 1. Získání druhé hodnoty
    other_value = getattr(other, "value", other)

    # 2. Pokus o standardní výpočet a vytvoření nové instance
    try:
        value = op(self.value, other_value)
        return with_composite(self, self.meta.name_snake, value)

    # 3. Pokus o přetypování
    except TypeError:

        # 3.1 Přetypování
        coerced = align_operand_type(self, other_value)

        # 3.2 Pokus o nový výpočet
        try:
            value = op(self.value, coerced)
            return with_composite(self, self.meta.name_snake, value)

        # 3.3 Vyvolání výjimky při neúspěchu
        except TypeError:
            return NotImplemented