from typing import TYPE_CHECKING, Any
# Outers
from ..base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...protocols.instance import SimpleInstanceLike
    from ...protocols.alias_typings import ValidTypes


class MetaShortcuts(SimpleMixin):
    """
    Ergonomické zkratky pro často používané položky z metadata objektu.
    Nepřidává žádnou logiku – pouze zpřístupňuje vybrané informace
    přímo na instanci.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # -------------------------
    # Property - Identita objektu
    # -------------------------
    @property
    def name_snake(
        self: "SimpleInstanceLike"
    ) -> str:
        """Snake_case jméno třídy objektu."""
        return self.meta.name_snake

    # -------------------------
    # Property - Typová informace
    # -------------------------
    @property
    def value_type(
        self: "SimpleInstanceLike"
    ) -> ValidTypes:
        """Pythoní typ hodnoty, kterou objekt uchovává."""
        return self.meta.value_type

    @property
    def default(
        self: "SimpleInstanceLike"
    ) -> Any:
        """Výchozí hodnota objektu definovaná v metadatech."""
        return self.meta.default

    # -------------------------
    # Property - Struktura objektu
    # -------------------------
    @property
    def is_atom(
        self: "SimpleInstanceLike"
    ) -> bool:
        """True, pokud objekt představuje atom (nemá inners)."""
        return self.meta.is_constant

    @property
    def is_composite(
        self: "SimpleInstanceLike"
    ) -> bool:
        """True, pokud objekt představuje kompozici (má inners)."""
        return not self.meta.is_constant

    @property
    def is_decomposeable(
        self: "SimpleInstanceLike"
    ) -> bool:
        """True, pokud lze hodnotu objektu měnit rozkladem."""
        return getattr(self.meta, "is_decomposeable", False)

