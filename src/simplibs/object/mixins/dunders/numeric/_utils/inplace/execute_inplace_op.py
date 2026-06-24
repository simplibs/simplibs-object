# Outers
from ..common import align_operand_type



def execute_inplace_op(self, op, other):
    """
    Rychlý modulární exekutor pro in-place aritmetické operace.
    Extrahuje hodnotu, provede výpočet a bezpečně zapíše výsledek do self.value.
    Obsahuje fallback pro bezpečné srovnání typů (coercion).
    """

    # 1. Získání druhé hodnoty
    other_value = getattr(other, "value", other)

    # 2. Pokus o standardní výpočet
    try:
        self.value = op(self.value, other_value)
        return self

    # 3. Pokus o přetypování
    except TypeError:

        # 3.1 Přetypování
        coerced = align_operand_type(self, other_value)

        # 3.2 Pokus o nový výpočet
        try:
            self.value = op(self.value, coerced)
            return self

        # 3.3 Vyvolání výjimky při neúspěchu nebo dělení nulou
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    # 3.3 Vyvolání výjimky při dělení nulou
    except ZeroDivisionError:
        return NotImplemented