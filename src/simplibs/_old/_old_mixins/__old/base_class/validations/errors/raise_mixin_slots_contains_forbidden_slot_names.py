def raise_mixin_slots_contains_forbidden_slot_names(cls: type) -> None:
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

        # 2. Zakázané názvy slotů
        forbidden = {
            "_value",
            "_owner",
            "_inners",
            "_logic",
            "_decompose",
            "_recalculate_self",
            "_recalculate_inners",
            "value",
            "owner",
            "meta",
            "__metadata__",
        }

        # 3. Průnik
        forbidden_found = forbidden & slots_set

        if forbidden_found:
            name = next(iter(forbidden_found))

            raise SimpleObjectMixinError(
                error_name="MIXIN DEFINITION ERROR",
                value_label="Forbidden slot name",
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