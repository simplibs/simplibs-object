from typing import Protocol, runtime_checkable, Any
from collections.abc import Callable
# Inners
from .ImmutableMethodsProtocol import ImmutableMethodsProtocol


@runtime_checkable
class ImmutableMethodsWithInnersProtocol(
    ImmutableMethodsProtocol,
    Protocol
):
    """
    Protokol pro mixin ImmutableInnerMethods.

    Garantuje přítomnost dynamicky generovaných imutabilních metod (setterů)
    pro jednotlivé vnitřní prvky (např. `obj.with_uzel(value)`).
    Všechny tyto metody produkují novou transformovanou instanci (Self).
    """

    def __getattr__(self, name: str) -> Callable[[Any], Any]:
        """
        Dynamický fallback pro přístup k vygenerovaným metodám transformace sub-nodů
        (např. přístup k `obj.with_motor`).

        Garantuje, že výsledkem volání takto získané metody je nová,
        upravená imutabilní instance stejného typu (Self).
        """
        ...