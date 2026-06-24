from typing import Protocol, runtime_checkable, Any, Callable, Self
# Inners
from .ImmutableMethodsProtocol import ImmutableMethodsProtocol


@runtime_checkable
class ImmutableInnerMethodsProtocol(ImmutableMethodsProtocol, Protocol):
    """
    Protokol pro mixin ImmutableInnerMethods.

    Garantuje přítomnost dynamicky generovaných imutabilních metod (setterů)
    pro jednotlivé vnitřní prvky (např. `obj.with_uzel(value)`).
    Všechny tyto metody produkují novou transformovanou instanci (Self).
    """

    # Samotný mixin nemá žádné vlastní sloty, metody vznikají až za běhu.

    def __getattr__(self, name: str) -> Callable[[Any], Self]:
        """
        Dynamický fallback pro přístup k vygenerovaným metodám transformace sub-nodů
        (např. přístup k `obj.with_motor`).

        Garantuje, že výsledkem volání takto získané metody je nová,
        upravená imutabilní instance stejného typu (Self).
        """
        ...