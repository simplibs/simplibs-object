from ......exceptions import SimpleObjectMixinError


def validate_mixin_is_simple_base_subclass(cls: type, mixin: type) -> None:
    """
    Validuje, že mixin je potomek SimpleMixin.
    """

    # Podmínka, která vede k vyvolání výjimky:
    # if not issubclass(mixin, SimpleMixin):

    from ......mixins.base_class import SimpleMixin

    if not issubclass(mixin, SimpleMixin):

        raise SimpleObjectMixinError(
            error_name="INVALID MIXIN",
            value_label="Mixin must inherit from SimpleMixin",
            expected="Třídu odvozenou od SimpleMixin.",
            value=mixin,
            problem=(
                f"Třída '{mixin.__name__}' není potomkem SimpleMixin a nemůže být "
                f"použita jako mixin pro třídu '{cls.__name__}'."
            ),
            context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
            how_to_fix=(
                "Ujistěte se, že mixin dědí ze SimpleMixin.",
                "Příklad:",
                "    class MyMixin(SimpleMixin):",
                "        __slots__ = ()",
                "",
                "Pokud mixin nemá být Simple mixin, nepředávejte jej do create_instance."
            ),
            exception=TypeError
        )
