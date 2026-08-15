from typing import Protocol, runtime_checkable
# Inners
from .IterableProtocol import IterableProtocol
from .MappingProtocol import MappingProtocol


@runtime_checkable
class CollectionProtocol(
    IterableProtocol,
    MappingProtocol,
    Protocol
):
    """
    Protocol for the Collection mixin.

    Encompasses full collection capabilities for composite instances.
    Fully combines mapping (dict-like) API with comprehensive iteration interfaces.
    """

    # The mixin itself acts solely as a structural aggregator, declaring no additional slots or methods.
