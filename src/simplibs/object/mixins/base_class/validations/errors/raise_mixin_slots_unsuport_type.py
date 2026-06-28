from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_unsuport_type(
    cls: "SimpleMixinProtocol"
) -> None:
    """
    Validuje, že __slots__ je typu tuple nebo str.
    """
    slots = cls.__dict__["__slots__"]

    if not isinstance(slots, (tuple, str)):

        raise SimpleMixinError(
            error_name="MIXIN DEFINITION ERROR",
            value_label="Invalid __slots__ type",
            expected="__slots__ must be tuple or string.",
            value=slots,
            problem=(
                f"Mixin '{cls.__name__}' má neplatný typ '__slots__': "
                f"{type(slots).__name__}."
            ),
            context=f"Kontrola definice mixinu: {cls.__name__}",
            how_to_fix=(
                "Použijte tuple nebo string pro definici __slots__.",
                "Příklad: __slots__ = ('a', 'b')",
                "Příklad: __slots__ = 'a'"
            ),
            exception=TypeError
        )
