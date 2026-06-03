from ........exceptions import SimpleMixinError


def raise_mixin_slots_is_not_defined(cls: type) -> None:
    """
    Validuje, že mixin definuje vlastní __slots__ a nezdědil je.
    """

    if "__slots__" not in cls.__dict__:

        raise SimpleMixinError(
            error_name="MIXIN DEFINITION ERROR",
            value_label="Missing __slots__ definition",
            expected="Mixin must define its own __slots__ (not inherited).",
            value=cls.__name__,
            problem=(
                f"Mixin '{cls.__name__}' neobsahuje vlastní definici '__slots__'. "
                "Zděděné slots nejsou povoleny."
            ),
            context=f"Kontrola definice mixinu: {cls.__name__}",
            how_to_fix=(
                "Přidejte do mixinu vlastní definici __slots__.",
                "Příklad: __slots__ = ('my_attr',)",
                "Zajistěte, aby __slots__ nebyly zděděné z rodičovské třídy."
            ),
            exception=TypeError
        )
