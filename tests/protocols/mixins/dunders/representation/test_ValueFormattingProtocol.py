from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class ValueFormattingProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Conversion (původní Representation).

    Garantuje podporu pro f-string formátování pomocí masek z metadat
    a nativní konverze objektu na typy bytes a bool na základě jeho vnitřní hodnoty.
    """

    def format(self, pattern: str | None = None) -> str:
        """
        Zformátuje vnitřní hodnotu instance podle zadaného patternu
        nebo masky definované v metadatach.
        """
        ...

    def __format__(self, format_spec: str = "") -> str:
        """
        Podpora pro f-string formátování. Umožňuje zápis f"{obj:pattern}".
        """
        ...

    def __bytes__(self) -> bytes:
        """
        Nativní převod vnitřní hodnoty instance na bajty (bytes).
        Pro nekompatibilní typy vyvolá TypeError.
        """
        ...

    def __bool__(self) -> bool:
        """
        Vrací pravdivostní hodnotu objektu vyhodnocenou z jeho vnitřní hodnoty.
        """
        ...