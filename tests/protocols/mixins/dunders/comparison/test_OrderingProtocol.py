from typing import Protocol, runtime_checkable, Any
# Outers
from ...base_class import SimpleMixinProtocol


@runtime_checkable
class OrderingProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protokol pro mixin Ordering.

    Garantuje kompletní sadu operátorů pro porovnávání velikosti (uspořádání)
    mezi instancemi navzájem nebo instancí a surovou hodnotou.
    """

    def __lt__(self, other: Any) -> bool:
        """Operátor 'menší než' (<). Porovnává na základě vnitřní hodnoty."""
        ...

    def __le__(self, other: Any) -> bool:
        """Operátor 'menší nebo rovno' (<=). Porovnává na základě vnitřní hodnoty."""
        ...

    def __gt__(self, other: Any) -> bool:
        """Operátor 'větší než' (>). Porovnává na základě vnitřní hodnoty."""
        ...

    def __ge__(self, other: Any) -> bool:
        """Operátor 'větší nebo rovno' (>=). Porovnává na základě vnitřní hodnoty."""
        ...