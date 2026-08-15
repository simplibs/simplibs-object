from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.representation import ValueDisplayProtocol


class ValueDisplay(SimpleMixin):
    """
    Přepíše __repr__ a __str__ tak, aby objekt vystupoval
    jako surová hodnota kterou obaluje.

    Změní způsob zobrazení objektu tak, aby reprezentoval svou hodnotu.
    Určeno pouze pro atomické (constant-only) typy, které se mají chovat
    jako „value-like“ objekty (např. Decimal, UUID, PhoneNumber…).

    ValueReprMixin je common, ale není to standardní mixin,
    nýbrž specializovaný, opt‑in, constant‑only mixin,
    který má být použit jen tehdy, když chceš,
    aby se objekt choval jako „value object“
    (např. Decimal, UUID, Path, Enum, …).

    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice určení
    _constant_only = True

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods - REPR / STR
    # ----------------------------------------

    def __repr__(
        self: "ValueDisplayProtocol"
    ) -> str:
        """
        Technická reprezentace objektu ve formátu:
            ClassName(value_repr)
        Používá se pro debugging a logování.
        """
        return f"{self.meta.class_name}({self.value!r})"

    def __str__(
        self: "ValueDisplayProtocol"
    ) -> str:
        """
        Uživatelská reprezentace objektu.
        Vrací čistou hodnotu převedenou na řetězec.
        """
        return str(self.value)