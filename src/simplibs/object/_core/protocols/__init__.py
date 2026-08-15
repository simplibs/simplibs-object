# Alias Typings Sub-Package
from . import alias_typings
# Classes
from .classes import (
    SimpleBaseProtocol,
    SimpleClassLike,
    SimpleClassType,
    SimpleConstantProtocol,
    SimpleObjectProtocol,
)
# Instance Core & Public
from .instance import (
    AtomInstanceProtocol,
    CompositeInstanceProtocol,
    InstanceBaseProtocol,
    SimpleConstantInstanceProtocol,
    SimpleInstanceBaseProtocol,
    SimpleInstanceClassLike,
    SimpleInstanceClassType,
    SimpleInstanceLike,
    SimpleInstanceType,
    SimpleObjectInstanceProtocol,
)
# Metadata
from .metadata import (
    SimpleBaseMetadataProtocol,
    SimpleConstantMetadataProtocol,
    SimpleMetadataLike,
    SimpleMetadataType,
    SimpleMetaProtocol,
    SimpleObjectMetadataProtocol,
)
# Methods
from .methods import (
    ClassMethodProtocol,
    LogicSignature, P, R,
)
# Mixins Sub-Package
from . import mixins
from .mixins import SimpleMixinLike
SimpleMixinType = SimpleMixinLike

__all__ = [
    # Sub-Package Modules
    "alias_typings",
    "mixins",

    # Classes Protocols & Aliases
    "SimpleBaseProtocol",
    "SimpleConstantProtocol",
    "SimpleObjectProtocol",
    "SimpleClassLike",
    "SimpleClassType",
    "SimpleMixinLike",
    "SimpleMixinType",

    # Instance Protocols & Aliases
    "InstanceBaseProtocol",
    "AtomInstanceProtocol",
    "CompositeInstanceProtocol",
    "SimpleInstanceBaseProtocol",
    "SimpleConstantInstanceProtocol",
    "SimpleObjectInstanceProtocol",
    "SimpleInstanceClassLike",
    "SimpleInstanceClassType",
    "SimpleInstanceLike",
    "SimpleInstanceType",

    # Metadata Protocols & Aliases
    "SimpleBaseMetadataProtocol",
    "SimpleConstantMetadataProtocol",
    "SimpleObjectMetadataProtocol",
    "SimpleMetaProtocol",
    "SimpleMetadataLike",
    "SimpleMetadataType",

    # Methods
    "ClassMethodProtocol",
    "LogicSignature", "P", "R"
]

_DESIGN_NOTES = """
# Protocols Main Architectural Entry-Point

## Purpose
Root interface package aggregating all structural contracts, type hints, metadata specifications, 
class/instance protocols, and mixin behavioral definitions across the entire framework.

## Internal Components Registry

| Component                        | Type      | Category     | Description                                                                  |
| :------------------------------- | :-------- | :----------- | :--------------------------------------------------------------------------- |
| `alias_typings`                  | Module    | Sub-Package  | Re-exported sub-package for domain-specific type aliases and typing helpers. |
| `mixins`                         | Module    | Sub-Package  | Re-exported sub-package for all behavioral mixin protocols and dunders.      |
| `SimpleBaseProtocol`             | Protocol  | Classes      | Foundational protocol for definition template classes.                      |
| `SimpleConstantProtocol`         | Protocol  | Classes      | Contract for atomic constant definition classes.                             |
| `SimpleObjectProtocol`           | Protocol  | Classes      | Contract for composite object definition classes.                            |
| `SimpleClassLike`                | TypeAlias | Classes      | Superset annotation for definition classes (`SimpleObjectProtocol`).        |
| `SimpleClassType`                | TypeAlias | Classes      | Minimal verification type for definition classes (`SimpleBaseProtocol`).     |
| `InstanceBaseProtocol`           | Protocol  | Instance     | Structural anchor for low-level runtime instances.                           |
| `AtomInstanceProtocol`           | Protocol  | Instance     | Core interface for atomic leaf instances with value management.              |
| `CompositeInstanceProtocol`      | Protocol  | Instance     | Core interface for composite instances with dynamic node access.             |
| `SimpleInstanceBaseProtocol`     | Protocol  | Instance     | Root protocol for factory-instantiated runtime objects.                      |
| `SimpleConstantInstanceProtocol` | Protocol  | Instance     | Complete protocol for final constant/atomic runtime instances.               |
| `SimpleObjectInstanceProtocol`   | Protocol  | Instance     | Complete protocol for final composite runtime instances.                     |
| `SimpleInstanceClassLike`        | TypeAlias | Instance     | Superset annotation for instance core classes (`CompositeInstanceProtocol`). |
| `SimpleInstanceClassType`        | TypeAlias | Instance     | Minimal type for instance core classes (`AtomInstanceProtocol`).             |
| `SimpleInstanceLike`             | TypeAlias | Instance     | Superset annotation for full instances (`SimpleObjectInstanceProtocol`).     |
| `SimpleInstanceType`             | TypeAlias | Instance     | Minimal type for full instances (`SimpleConstantInstanceProtocol`).          |
| `SimpleBaseMetadataProtocol`     | Protocol  | Metadata     | Base contract for metadata structures and namespace specs.                  |
| `SimpleConstantMetadataProtocol` | Protocol  | Metadata     | Specification protocol for atomic constants metadata.                       |
| `SimpleObjectMetadataProtocol`   | Protocol  | Metadata     | Specification protocol for composite nodes metadata.                         |
| `SimpleMetaProtocol`             | Protocol  | Metadata     | Contract for metaclasses injecting metadata and instance factories.          |
| `SimpleMetadataLike`             | TypeAlias | Metadata     | Superset annotation for metadata (`SimpleObjectMetadataProtocol`).          |
| `SimpleMetadataType`             | TypeAlias | Metadata     | Minimal verification type for metadata (`SimpleBaseMetadataProtocol`).       |
| `ClassMethodProtocol`            | Protocol  | Methods      | Interface for custom class-bound methods and executable hooks.               |
| `LogicSignature`                 | TypeAlias | Methods      | Callable signature alias for computational logic functions.                  |
"""