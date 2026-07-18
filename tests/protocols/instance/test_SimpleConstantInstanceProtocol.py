from typing import Protocol, runtime_checkable
# Inners
from .core_classes import AtomInstanceProtocol
from .SimpleInstanceBaseProtocol import SimpleInstanceBaseProtocol


@runtime_checkable
class SimpleConstantInstanceProtocol(
    AtomInstanceProtocol,
    SimpleInstanceBaseProtocol,
    Protocol
):
    """Protokol pro kompozitní konečnou instanci (bez mixinů)"""
