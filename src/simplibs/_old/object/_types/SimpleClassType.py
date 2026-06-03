from typing import Protocol, Type
# Inners
from .SimpleMetaType import SimpleMetaType


class SimpleClassType(Protocol):
    """
    Protokol, který simuluje minimální rozhraní třídy
    v systému Simple pro potřeby statické analýzy.
    """
    # Naše vlastní metadata
    meta: SimpleMetaType
    __metadata__: SimpleMetaType

    # Standardní atributy třídy, které potřebujeme v builderech
    __name__: str
    __mro__: tuple[type, ...]
    __bases__: tuple[type, ...]

