from .SimpleMetaProtocol import SimpleMetaProtocol
from .SimpleBaseMetadataProtocol import SimpleBaseMetadataProtocol
from .SimpleConstantMetadataProtocol import SimpleConstantMetadataProtocol
from .SimpleObjectMetadataProtocol import SimpleObjectMetadataProtocol

# Element defining the largest set (superset for annotations)
SimpleMetadataLike = SimpleObjectMetadataProtocol

# Element defining the smallest set (minimal interface for type verification)
SimpleMetadataType = SimpleBaseMetadataProtocol


_DESIGN_NOTES = """
# Metadata Protocols Sub-Package

## Purpose
Defines protocols for metadata structures and metaclass interfaces, ensuring strict structural contracts
for class specifications, naming registries, and lazy-loaded instance class factories.

## Internal Components Registry

| Component                        | Type     | Description                                                              |
| :------------------------------- | :------- | :----------------------------------------------------------------------- |
| `SimpleBaseMetadataProtocol`     | Protocol | Base metadata contract defining owner references and namespace naming.   |
| `SimpleConstantMetadataProtocol` | Protocol | Specification protocol for atomic constants and default validations.     |
| `SimpleObjectMetadataProtocol`   | Protocol | Specification protocol for composite nodes and inner element maps.     |
| `SimpleMetaProtocol`             | Protocol | Contract for the metaclass injecting metadata and `__call__` factory.    |
"""