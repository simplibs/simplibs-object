from typing import TYPE_CHECKING
# Outers
from ...._common.constants import FORBIDDEN_NAMES
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_contains_forbidden_slot_names(
    cls: "SimpleMixinProtocol"
) -> None:
        """
        Validuje, že mixin nedefinuje zakázané názvy slotů.
        """
        slots = cls.__dict__["__slots__"]
        # 1. Převod slotů na množinu
        if isinstance(slots, str):
            slots_set = {slots}
        elif isinstance(slots, tuple):
            slots_set = set(slots)
        else:
            # Tohle by mělo být ošetřeno v jiné validaci
            return

        # Průnik
        forbidden_found = FORBIDDEN_NAMES & slots_set

        if forbidden_found:
            name = next(iter(forbidden_found))

            raise SimpleMixinError(
                error_name="MIXIN DEFINITION ERROR",
                label="Forbidden slot name",
                expected="Mixin must not define slots that collide with internal Simple attributes.",
                value=name,
                problem=(
                    f"Mixin '{cls.__name__}' definuje slot '{name}', "
                    "který je interní součástí Simple systému."
                ),
                context=f"Kontrola definice mixinu: {cls.__name__}",
                how_to_fix=(
                    f"Odstraňte slot '{name}' z __slots__ mixinu.",
                    "Použijte vlastní unikátní jména slotů, která nekolidují s interními atributy.",
                    "Doporučení: prefixujte sloty mixinů např. '_mx_' nebo '_mixin_'."
                ),
                exception=TypeError
            )