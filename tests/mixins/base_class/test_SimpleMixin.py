from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .validations import verify_mixin_definition
# Annotations
if TYPE_CHECKING:
    from ...protocols.mixins.base_class import SimpleMixinProtocol
    from ...protocols.alias_typings import ValidTypes


class SimpleMixin:
    """
    Třída reprezentující základní rozhraní pro všechny mixiny v systému Simple.

    Deklaruje přítomnost inicializační metody a konfiguračních flagů, které
    řídí, na jaké typy instancí smí být mixin v továrně aplikován.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Deklarativní omezení
    _constant_only = False
    _composite_only = False
    _mutable_only = False
    _immutable_only = False
    _only_types: "ValidTypes" = UNSET

    # Definice sltu
    __slots__ = ()

    # ----------------------------------------
    # Hook pro inicializaci
    # ----------------------------------------

    # noinspection PyUnresolvedReferences
    def init_mixins(
        self: "SimpleMixinProtocol"
    ) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""

        # 1. Inicializace předků
        super().init_mixins()

    # ----------------------------------------
    # Metoda pro kontrolu zapsaných dat
    # ----------------------------------------

    def __init_subclass__(
        cls: "SimpleMixinProtocol",
        **kwargs
    ) -> None:
        """Validuje zapsané data."""

        # 1. Inicializace kontroly předků
        super().__init_subclass__(**kwargs)

        # 2. Ověření zadaných dat mixinu
        verify_mixin_definition(cls)

