from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ....protocols.mixins.dunders.representation import ValueDisplayProtocol


class ValueFormatting(SimpleMixin):
    """
    Reprezentační a konverzní dundery navázané na hodnotu objektu.
    Nezasahuje do __repr__ / __str__ – ty jsou definované v InstanceBase.
    Funguje pro atomické i kompozitní typy, protože oba mají hodnotu.
    """

    # ----------------------------------------
    # Základní rozhraní
    # ----------------------------------------

    # Definice slotů
    __slots__ = ()

    # ----------------------------------------
    # Methods = FORMAT
    # ----------------------------------------

    def format(
        self: "ValueDisplayProtocol",
        pattern: str | None = None
    ) -> str:
        """
        Zformátuje hodnotu instance podle zadaného patternu.
        Pokud není pattern zadán, použije masku z metadat (meta.mask),
        pokud existuje. Vhodné pro formátování čísel, textů a jednoduchých
        hodnot kompozic.
        """
        value = self.value
        mask = pattern or getattr(self.meta, "mask", None)

        if mask and isinstance(value, (str, int, float)):
            return mask.format(value)

        return str(value)

    def __format__(
        self,
        format_spec: str = ""
    ) -> str:
        """
        Podpora pro f-string formátování.
        Umožňuje zápis typu: f"{obj:pattern}".
        """
        return self.format(format_spec or None)

    # ----------------------------------------
    # Methods = BYTES / BOOL
    # ----------------------------------------

    def __bytes__(
        self: "ValueDisplayProtocol"
    ) -> bytes:
        """
        Převod hodnoty instance na bytes.
        Podporuje:
            - bytes → vrací přímo
            - bytearray, memoryview → bytes(...)
            - str → UTF-8 encode
        Ostatní typy vyvolají TypeError.
        """
        value = self.value

        if isinstance(value, bytes):
            return value

        if isinstance(value, (bytearray, memoryview)):
            return bytes(value)

        if isinstance(value, str):
            return value.encode("utf-8")

        raise TypeError(
            f"Nelze převést {self.meta.class_name} "
            f"(type={type(value).__name__}) na bytes."
        )

    def __bool__(
        self: "ValueDisplayProtocol"
    ) -> bool:
        """
        Pravdivost objektu odpovídá pravdivosti jeho hodnoty.
        """
        return bool(self.value)

