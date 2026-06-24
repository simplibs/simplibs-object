# Outers
from .....immutable._utils.immutable_methods.with_constant import with_constant


def execute_bit_rop(self, op, other):
    """Rychlý modulární exekutor pro pravostranné bitové operace (other_value op self.value)."""

    # 1. Získání druhé hodnoty
    other_value = getattr(other, "value", other)

    # 2. Pokus o výpočet
    try:
        return with_constant(self, self.meta.name_snake, op(other_value, self.value))

    # 3. Vyvolání výjimky při neúspěchu
    except TypeError:
        return NotImplemented