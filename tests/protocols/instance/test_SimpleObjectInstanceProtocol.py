from typing import Protocol, runtime_checkable
# Inners
from .core_classes import CompositeInstanceProtocol
from .SimpleInstanceBaseProtocol import SimpleInstanceBaseProtocol


@runtime_checkable
class SimpleObjectInstanceProtocol(
    CompositeInstanceProtocol,
    SimpleInstanceBaseProtocol,
    Protocol
):
    """Protokol pro kompozitní konečnou instanci (bez mixinů)"""

