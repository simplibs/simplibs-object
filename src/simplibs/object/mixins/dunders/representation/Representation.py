class Representation(SimpleMixin):
    """
    Reprezentační a konverzní dundery navázané na hodnotu objektu.
    Nezasahuje do __repr__ / __str__ – ty jsou definované v InstanceBase.
    """

    __slots__ = ()

    def format(self, pattern: str | None = None) -> str:
        """
        Zformátuje hodnotu. Pokud není pattern zadán, zkusí ho najít
        v metadatech (meta.mask). Příklad: "+420 {}" pro telefonní číslo.
        """
        value = self.value
        mask = pattern or getattr(self.meta, "mask", None)

        if mask and isinstance(value, (str, int, float)):
            return mask.format(value)

        return str(value)

    def __format__(self, format_spec: str = "") -> str:
        """Podpora pro f-stringy: f"{obj:maska}" """
        return self.format(format_spec or None)

    def __bytes__(self) -> bytes:
        """
        Převod hodnoty na bytes.
        Podporuje: bytes, bytearray, memoryview → bytes(...)
                   str → encode('utf-8')
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

    def __bool__(self) -> bool:
        """Pravdivost objektu odpovídá pravdivosti jeho hodnoty."""
        return bool(self.value)