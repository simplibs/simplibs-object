def raise_mixin_dict_contains_forbidden_attributes(cls: type) -> None:
    """
    Validuje, že mixin nepřepisuje zakázané atributy.
    """

    forbidden = {"_value", "_owner", "value", "owner"}

    for name in forbidden:
        if name in cls.__dict__:

            raise SimpleMixinError(
                error_name="MIXIN DEFINITION ERROR",
                value_label="Forbidden attribute override",
                expected="Mixin must not define or override internal Simple attributes.",
                value=name,
                problem=(
                    f"Mixin '{cls.__name__}' definuje zakázaný atribut '{name}'. "
                    "Tento atribut je interní součástí Simple systému."
                ),
                context=f"Kontrola definice mixinu: {cls.__name__}",
                how_to_fix=(
                    f"Odstraňte atribut '{name}' z mixinu.",
                    "Pokud potřebujete vlastní stav, použijte __slots__ "
                    "a definujte vlastní jména atributů."
                ),
                exception=TypeError
            )
