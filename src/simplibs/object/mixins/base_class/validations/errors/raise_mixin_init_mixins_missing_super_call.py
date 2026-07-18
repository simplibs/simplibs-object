from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_init_mixins_missing_super_call(
    cls: "SimpleMixinProtocol"
) -> None:
    """
    Validuje, že metoda init_mixins obsahuje volání super().init_mixins().
    """

    if "init_mixins" not in cls.__dict__:
        return  # mixin nepřepisuje init_mixins → OK

    func = cls.__dict__["init_mixins"]

    # 1. Získání jmen volaných uvnitř metody
    called_names = func.__code__.co_names

    # 2. Kontrola přítomnosti super() i init_mixins
    if "super" not in called_names or "init_mixins" not in called_names:

        raise SimpleObjectMixinError(
            error_name="MIXIN DEFINITION ERROR",
            label="Missing super() call in init_mixins",
            expected="Metoda init_mixins musí volat super().init_mixins().",
            value=func,
            problem=(
                f"Mixin '{cls.__name__}' přepisuje metodu 'init_mixins', "
                "ale nevolá super().init_mixins(). "
                "Tím dochází k přerušení řetězení mixin inicializace."
            ),
            context=f"Kontrola definice mixinu: {cls.__name__}",
            how_to_fix=(
                "Přidejte volání super().init_mixins() do metody init_mixins.",
                "Příklad:",
                "    def init_mixins(self):",
                "        super().init_mixins()",
                "        # vaše logika zde"
            ),
            exception=TypeError
        )
