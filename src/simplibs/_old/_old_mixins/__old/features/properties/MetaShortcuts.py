# Outers
from ....protocols import SimpleInstanceType
from ...base_class import SimpleMixin


class MetaShortcuts(SimpleMixin):
    """
    Ergonomické zkratky pro často používané položky z metadata objektu.
    Nepřidává žádnou logiku – pouze zpřístupňuje vybrané informace
    přímo na instanci.
    """

    __slots__ = ()

    # -------------------------
    # Identita objektu
    # -------------------------
    @property
    def name_snake(self: SimpleInstanceType) -> str:
        """Snake_case jméno třídy objektu."""
        return self.meta.name_snake

    # -------------------------
    # Typová informace
    # -------------------------
    @property
    def value_type(self: SimpleInstanceType) -> type:
        """Pythoní typ hodnoty, kterou objekt uchovává."""
        return self.meta.value_type

    @property
    def default(self: SimpleInstanceType):
        """Výchozí hodnota objektu definovaná v metadatech."""
        return self.meta.default

    # -------------------------
    # Struktura objektu
    # -------------------------
    @property
    def is_atom(self: SimpleInstanceType) -> bool:
        """True, pokud objekt představuje atom (nemá inners)."""
        return self.meta.is_constant

    @property
    def is_composite(self: SimpleInstanceType) -> bool:
        """True, pokud objekt představuje kompozici (má inners)."""
        return not self.meta.is_constant

    @property
    def is_decomposeable(self: SimpleInstanceType) -> bool:
        """True, pokud lze hodnotu objektu měnit rozkladem."""
        return getattr(self.meta, "is_decomposeable", False)
