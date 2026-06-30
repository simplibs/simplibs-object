from typing import TYPE_CHECKING
# Outers
from .......exceptions import SimpleObjectMixinError
# Annotations
if TYPE_CHECKING:
    from .......protocols.classes import SimpleClassLike
    from .......protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_slots_conflict_error(
    cls: "SimpleClassLike",
    mixins: tuple["SimpleMixinProtocol", ...],
    error: TypeError
) -> None:
    """
    Vyvolá výjimku při kolizi __slots__ mezi mixiny během skládání instanční třídy.
    """

    # Podmínka, která vede k vyvolání výjimky:
    # except TypeError as error:  # kolize slotů mezi mixiny

    mixin_names = ", ".join(m.__name__ for m in mixins)

    raise SimpleObjectMixinError(
        error_name="MIXIN SLOTS CONFLICT",
        value_label="Slot name collision between mixins",
        expected="Mixiny s nekolidujícími __slots__.",
        value=error,
        problem=(
            "Došlo ke kolizi __slots__ mezi mixiny při skládání instanční třídy. "
            "Python vyhodil TypeError, protože dva nebo více mixinů definují "
            "stejné jméno slotu nebo jinak nekompatibilní sloty."
        ),
        context=(
            f"create_instance(cls={cls.__name__}, mixins=({mixin_names}))"
        ),
        how_to_fix=(
            "Zkontrolujte definice __slots__ ve všech mixinech, které používáte.",
            "Ujistěte se, že žádné dva mixiny nedefinují stejné jméno slotu.",
            "Příklad správného použití:",
            "    class MixinA(SimpleMixin):",
            "        __slots__ = ('a',)",
            "",
            "    class MixinB(SimpleMixin):",
            "        __slots__ = ('b',)",
            "",
            "Pokud mixiny sdílejí logiku, která potřebuje stejné jméno slotu, "
            "zvažte jejich sloučení nebo refaktorování.",
        ),
        exception=TypeError
    )
