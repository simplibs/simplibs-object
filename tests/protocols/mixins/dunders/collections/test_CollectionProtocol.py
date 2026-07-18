from typing import Protocol, runtime_checkable
# Inners
from .CollectionIterableProtocol import CollectionIterableProtocol
from .CollectionMappingProtocol import CollectionMappingProtocol


@runtime_checkable
class CollectionProtocol(
    CollectionIterableProtocol,
    CollectionMappingProtocol,
    Protocol
):
    """
    Protokol pro mixin Collection.

    Zastřešuje kompletní kolekční chování pro kompozitní instance.
    Plně kombinuje mapovací (dict-like) API i komplexní iterační rozhraní.
    """

    # Samotný mixin je pouze strukturální spojka, nemá žádné vlastní sloty ani metody.