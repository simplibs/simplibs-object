from numbers import Integral


def coerce(self, value):
    """
    Pokusí se převést hodnotu na typ defaultní hodnoty,
    ale pouze pokud je to bezpečné.

    Bezpečné konverze:
    - int → float
    - int → Decimal
    - int → Fraction

    Nebezpečné konverze (NEPROVÁDÍME):
    - float → int
    - float → Decimal (kvůli rounding error)
    - Fraction → int
    - Decimal → int
    """
    target_type = type(self.meta.default)

    # Bezpečné: int → širší typ
    if isinstance(value, Integral) and target_type is not int:
        try:
            return target_type(value)
        except Exception:
            return value

    # Jinak nekonvertujeme
    return value
