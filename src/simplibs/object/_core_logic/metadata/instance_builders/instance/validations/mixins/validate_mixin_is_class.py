from ......exceptions import SimpleObjectMixinError


def validate_mixin_is_class(cls: type, mixin: object) -> None:
    """
    Validuje, že mixin je třída (nikoli instance, funkce, modul, atd.).
    """

    # Podmínka, která vede k vyvolání výjimky:
    # if not isinstance(mixin, type):

    if not isinstance(mixin, type):

        raise SimpleObjectMixinError(
            error_name="INVALID MIXIN",
            value_label="Mixin must be a class",
            expected="Třídu odvozenou od SimpleMixin.",
            value=mixin,
            problem=(
                f"Objekt '{mixin!r}' není třída a nemůže být použit jako mixin "
                f"pro třídu '{cls.__name__}'."
            ),
            context=f"create_instance(cls={cls.__name__}, mixin={mixin!r})",
            how_to_fix=(
                "Ujistěte se, že předáváte třídu, nikoli instanci nebo jiný objekt.",
                "Příklad správného použití:",
                "    create_instance(MyClass, mixins=(MyMixin,), as_atom=False)"
            ),
            exception=TypeError
        )
