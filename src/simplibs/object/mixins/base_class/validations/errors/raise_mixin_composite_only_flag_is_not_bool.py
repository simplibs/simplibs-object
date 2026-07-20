from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .....protocols.mixins.base_class import SimpleMixinProtocol


def raise_mixin_composite_only_flag_is_not_bool(
    cls: "SimpleMixinProtocol"
) -> None:
    """
    Validuje, že mixin definuje _composite_only správně (pokud jej definuje).
    """

    # 1. Kontrola, zda je flag definovaný přímo na mixinu
    if "_composite_only" not in cls.__dict__:
        return  # není definovaný → OK

    composite_only = cls.__dict__["_composite_only"]

    # 2. Musí být typu bool
    if not isinstance(composite_only, bool):

        raise SimpleMixinError(
            error_name="MIXIN DEFINITION ERROR",
            label="Invalid _composite_only flag",
            expected="Hodnota _composite_only musí být typu bool (True/False).",
            value=composite_only,
            problem=(
                f"Mixin '{cls.__name__}' definuje '_composite_only', ale jeho hodnota "
                f"není typu bool."
            ),
            context=f"Kontrola definice mixinu: {cls.__name__}",
            how_to_fix=(
                "Upravte hodnotu '_composite_only' na True nebo False.",
                "Příklad: _composite_only = True",
                "Pokud flag nepotřebujete, odstraňte jej z mixinu."
            ),
            exception=TypeError
        )