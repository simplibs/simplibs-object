# Base Class
from .base_class import (
    SimpleMixinProtocol,
    SimpleMixinLike

)
# Core Mixins
from .core_mixins import (
    InfrastructureProtocol,
    NodesDictsProtocol,
    NodesTupleProtocol,
    SerializationProtocol,
    SnapshotProtocol,
)
# Dunders Sub-Package
from . import dunders
# Immutable
from .immutable import (
    ImmutableMethodsProtocol,
    ImmutableMethodsWithInnersProtocol,
)
# Numerical & Stepper
from .numerical import (
    EqualizerProtocol,
    VolumeProtocol,
)
from .numerical.internal_types import (
    SteppersMap,
)
from .numerical.stepper import (
    StepperProtocol,
)
from .numerical.stepper.internal_types import (
    LimitAction,
    StepValue,
)
# Properties
from .properties import (
    InnersPropertyProtocol,
    MetaShortcutsProtocol,
)
# State
from .state import (
    DefaultStateProtocol,
    DirtyTrackingProtocol,
    HistoryProtocol,
    PermissionProtocol,
)

__all__ = [
    # Base Class
    "SimpleMixinProtocol",
    "SimpleMixinLike",

    # Core Mixins
    "InfrastructureProtocol",
    "NodesDictsProtocol",
    "NodesTupleProtocol",
    "SerializationProtocol",
    "SnapshotProtocol",

    # Dunders Sub-Package Re-export Module
    "dunders",

    # Immutable
    "ImmutableMethodsProtocol",
    "ImmutableMethodsWithInnersProtocol",

    # Numerical
    "EqualizerProtocol",
    "VolumeProtocol",
    "StepperProtocol",
    "SteppersMap",
    "LimitAction",
    "StepValue",

    # Properties
    "InnersPropertyProtocol",
    "MetaShortcutsProtocol",

    # State
    "DefaultStateProtocol",
    "DirtyTrackingProtocol",
    "HistoryProtocol",
    "PermissionProtocol",
]

_DESIGN_NOTES = """
# Mixin Protocols Main Package

## Purpose
Aggregates all architectural mixin protocols across the system, guaranteeing clear structural contracts 
for runtime behavior, core state operations, numerical manipulation, immutability, and state tracking.

## Internal Components Registry

| Component                             | Type      | Category     | Description                                                                  |
| :------------------------------------ | :-------- | :----------- | :--------------------------------------------------------------------------- |
| `SimpleMixinProtocol`                 | Protocol  | Base Class   | Foundational protocol for all mixin classes ensuring base initialization.     |
| `InfrastructureProtocol`             | Protocol  | Core Mixins  | Internal low-level utility and lifecycle mixin interface.                    |
| `NodesDictsProtocol`                  | Protocol  | Core Mixins  | Interface for managing named child nodes via dictionary representations.     |
| `NodesTupleProtocol`                  | Protocol  | Core Mixins  | Interface for accessing ordered composite child node tuples.                 |
| `SerializationProtocol`               | Protocol  | Core Mixins  | Pure serialization contract for exporting and importing instance data.       |
| `SnapshotProtocol`                    | Protocol  | Core Mixins  | Interface for creating and restoring full state snapshots.                   |
| `dunders`                             | Module    | Sub-Package  | Sub-package namespace re-exporting all Python magic method protocols.        |
| `ImmutableMethodsProtocol`           | Protocol  | Immutable    | Functional interface for state transformations returning new instances.       |
| `ImmutableMethodsWithInnersProtocol`  | Protocol  | Immutable    | Dynamic inner attribute fallback interface for setter generation.             |
| `EqualizerProtocol`                   | Protocol  | Numerical    | Multi-node numerical controller mapping interface.                            |
| `VolumeProtocol`                      | Protocol  | Numerical    | Single primary value stepper controller interface.                            |
| `StepperProtocol`                     | Protocol  | Numerical    | Encapsulated numeric stepping controller with bound verification.            |
| `SteppersMap`                         | TypeAlias | Numerical    | Dictionary mapping of snake_case names to respective Steppers.               |
| `LimitAction`                         | TypeAlias | Numerical    | Callback/action type invoked when hitting numerical boundaries.              |
| `StepValue`                           | TypeAlias | Numerical    | Shift delta value or Ellipsis (`...`) default indicator.                      |
| `InnersPropertyProtocol`              | Protocol  | Properties   | Interface exposing direct access to inner elements and structure.            |
| `MetaShortcutsProtocol`               | Protocol  | Properties   | Fast access shortcuts for metadata, system attributes, and tags.             |
| `DefaultStateProtocol`                | Protocol  | State        | Interface for state resets and initial value defaults restoration.           |
| `DirtyTrackingProtocol`               | Protocol  | State        | Interface for tracking modified fields and dirty flags across instances.     |
| `HistoryProtocol`                     | Protocol  | State        | Contract for undo/redo state stack traversal.                                |
| `PermissionProtocol`                  | Protocol  | State        | Access control contract for reading and writing instance values.             |
"""