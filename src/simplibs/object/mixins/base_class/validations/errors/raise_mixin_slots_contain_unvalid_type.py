from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_contain_unvalid_type(
    cls: "SimpleMixinProtocol"
) -> None:
    """
    Validuje, že tuple __slots__ obsahuje pouze stringy.
    """
    slots = cls.__dict__["__slots__"]
    if isinstance(slots, tuple):
        if not all(isinstance(s, str) for s in slots):

            raise SimpleMixinError(
                error_name="MIXIN DEFINITION ERROR",
                label="Invalid __slots__ items",
                expected="All items in __slots__ tuple must be strings.",
                value=slots,
                problem=(
                    f"Mixin '{cls.__name__}' má neplatné položky v '__slots__'. "
                    "Všechny položky musí být typu 'str'."
                ),
                context=f"Kontrola definice mixinu: {cls.__name__}",
                how_to_fix=(
                    "Upravte položky v __slots__ tak, aby byly všechny stringy.",
                    "Příklad: __slots__ = ('flag', 'counter')"
                ),
                exception=TypeError
            )
