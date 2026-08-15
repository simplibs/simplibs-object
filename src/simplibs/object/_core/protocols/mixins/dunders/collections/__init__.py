from .CollectionBaseProtocol import CollectionBaseProtocol
from .CollectionProtocol import CollectionProtocol
from .IterableProtocol import IterableProtocol
from .MappingProtocol import MappingProtocol

_DESIGN_NOTES = """
# Collections Dunder Protocols Sub-Package

## Purpose
Provides protocols defining container, mapping, and sequence behavior via standard Python dunder methods,
enabling clean container operations, iteration, and element accessing.

## Internal Components Registry

| Component                | Type     | Description                                                                  |
| :----------------------- | :------- | :--------------------------------------------------------------------------- |
| `CollectionBaseProtocol` | Protocol | Structural anchor for collection mixins with size and containment support.   |
| `CollectionProtocol`     | Protocol | Complete container interface combining sizing, containment, and iteration.  |
| `IterableProtocol`       | Protocol | Interface guaranteeing element iteration capability via `__iter__`.          |
| `MappingProtocol`        | Protocol | Key-value mapping interface with item retrieval, assignment, and deletion.   |
"""