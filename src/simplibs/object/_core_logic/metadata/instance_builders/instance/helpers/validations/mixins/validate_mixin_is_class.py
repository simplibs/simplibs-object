from typing import TYPE_CHECKING
# Outers
from ........exceptions import SimpleMixinError
# Annotations
if TYPE_CHECKING:
    from ........protocols.classes import SimpleClassLike

def validate_mixin_is_class(
    cls: "SimpleClassLike",
    mixin: object
) -> None:
    """
    Validuje, že mixin je třída (nikoli instance, funkce, modul, atd.).
    """

    # Podmínka, která vede k vyvolání výjimky:
    # if not isinstance(mixin, type):

    if not isinstance(mixin, type):

        raise SimpleMixinError(
            error_name="INVALID MIXIN",
            label="Mixin must be a class",
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
