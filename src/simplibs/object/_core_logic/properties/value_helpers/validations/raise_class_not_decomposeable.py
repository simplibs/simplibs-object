from typing import TYPE_CHECKING
# Outers
from ......exceptions import SimpleLogicError
# Annotations
if TYPE_CHECKING:
    from ......protocols.metadata import SimpleMetadataLike


def raise_class_not_decomposeable(
    meta: "SimpleMetadataLike"
) -> None:

    # !!Je potřeba ji dodefinovat - bylo zde:
    raise TypeError(
        f"Kompozice '{meta.class_name}' nepodporuje přímé přiřazení hodnoty, "
        f"protože nemá definovanou uživatelskou metodu decompose_value()."
    )

    # Podmínka, která vede k vyvolání výjimky:
    # if not issubclass(mixin, SimpleMixin):

    # raise SimpleLogicError(
    #     error_name="INVALID MIXIN",
    #     label="Mixin must inherit from SimpleMixin",
    #     expected="Třídu odvozenou od SimpleMixin.",
    #     value=mixin,
    #     problem=(
    #         f"Třída '{mixin.__name__}' není potomkem SimpleMixin a nemůže být "
    #         f"použita jako mixin pro třídu '{cls.__name__}'."
    #     ),
    #     context=f"create_instance(cls={cls.__name__}, mixin={mixin.__name__})",
    #     how_to_fix=(
    #         "Ujistěte se, že mixin dědí ze SimpleMixin.",
    #         "Příklad:",
    #         "    class MyMixin(SimpleMixin):",
    #         "        __slots__ = ()",
    #         "",
    #         "Pokud mixin nemá být Simple mixin, nepředávejte jej do create_instance."
    #     ),
    #     exception=TypeError
    # )
