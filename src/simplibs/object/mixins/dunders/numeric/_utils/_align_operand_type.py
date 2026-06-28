from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.base_class import SimpleMixinLike


# noinspection PyBroadException
def _align_operand_type(
    self: "SimpleMixinLike",
    value: Any
) -> Any:
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

    # 1. Načtení typu
    target_type = type(self.meta.default)

    # 2. Pokus o převod na stejný typ
    try:
        return target_type(value)

    # 3. Při neůspěchu vracíme stejnou hodnotu
    except Exception:
        return value
