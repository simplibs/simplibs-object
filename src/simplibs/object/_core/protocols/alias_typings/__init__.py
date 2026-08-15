# Changes
from .changes import (
    ChangesDict,
    ChangesTuple,
    ChangeTuple,
)
# History
from .history import (
    HistoryDict,
    HistoryEntry,
)
# Inners
from .inners import (
    InnersMap,
    InnersTuple,
)
# Mixins
from .mixins import (
    MixinsTuple,
)
# Names
from .names import (
    NamesSet,
    NamesTuple,
)
# Nodes
from .nodes import (
    NodeItem,
    NodesDict,
    NodesIndexMap,
    NodesInstanceDict,
    NodesPathDict,
    NodesTuple,
)
# Paths
from .paths import (
    PathDict,
    PathTuple,
)
# Snapshots
from .snapshots import (
    SnapshotDict,
    SnapshotDiffItem,
    SnapshotDiffTuple,
    SnapshotTuple,
)
# State
from .state import (
    StateDict,
)
# Types
from .types import (
    ValidTypes,
)

__all__ = [
    # Changes
    "ChangesDict",
    "ChangesTuple",
    "ChangeTuple",

    # History
    "HistoryDict",
    "HistoryEntry",

    # Inners
    "InnersMap",
    "InnersTuple",

    # Mixins
    "MixinsTuple",

    # Names
    "NamesSet",
    "NamesTuple",

    # Nodes
    "NodeItem",
    "NodesDict",
    "NodesIndexMap",
    "NodesInstanceDict",
    "NodesPathDict",
    "NodesTuple",

    # Paths
    "PathDict",
    "PathTuple",

    # Snapshots
    "SnapshotDict",
    "SnapshotDiffItem",
    "SnapshotDiffTuple",
    "SnapshotTuple",

    # State
    "StateDict",

    # Types
    "ValidTypes",
]

_DESIGN_NOTES = """
# Alias Typings Main Package

## Purpose
Central entry point for all domain-specific type aliases across changes, history, composition, 
snapshots, paths, nodes, and type validations.

## Internal Components Registry

| Component           | Type      | Category  | Description                                                                  |
| :------------------ | :-------- | :-------- | :--------------------------------------------------------------------------- |
| `ChangesDict`       | TypeAlias | Changes   | Key-value dictionary mapping element names to their new target values.       |
| `ChangesTuple`      | TypeAlias | Changes   | Tuple containing one or multiple change pairs for batch processing.          |
| `ChangeTuple`       | TypeAlias | Changes   | Pair structure `(element_name, new_value)` representing a single update.    |
| `HistoryDict`       | TypeAlias | History   | Serialized dictionary format holding the exported history data package.      |
| `HistoryEntry`      | TypeAlias | History   | Timestamped tuple entry `(datetime, SnapshotTuple)` recording a state point. |
| `InnersMap`         | TypeAlias | Inners    | Dictionary mapping snake_case component names to inner definition classes.   |
| `InnersTuple`       | TypeAlias | Inners    | Tuple holding declared inner component classes for composite architecture.   |
| `MixinsTuple`       | TypeAlias | Mixins    | Immutable tuple containing mixin protocol references applied to an object.   |
| `NamesSet`          | TypeAlias | Names     | Unordered set container storing unique registered element names.            |
| `NamesTuple`        | TypeAlias | Names     | Immutable ordered tuple holding registered element name strings.              |
| `NodeItem`          | TypeAlias | Nodes     | Pair structure `(live_instance, path_tuple)` representing a registered node. |
| `NodesDict`         | TypeAlias | Nodes     | Complex map associating node names with their `(instance, path)` pair.       |
| `NodesIndexMap`     | TypeAlias | Nodes     | Sequence index map storing original positional offsets for subnodes.          |
| `NodesInstanceDict` | TypeAlias | Nodes     | Direct lookup mapping snake_case names directly to live instances.           |
| `NodesPathDict`     | TypeAlias | Nodes     | Path mapping associating subnode names with their hierarchical path tuples.  |
| `NodesTuple`        | TypeAlias | Nodes     | Ordered sequence tuple holding all node items in a composite structure.      |
| `PathDict`          | TypeAlias | Paths     | Key-value dictionary mapping element identifiers to their path tuples.       |
| `PathTuple`         | TypeAlias | Paths     | Immutable tuple of string tokens representing a hierarchical path.           |
| `SnapshotDict`      | TypeAlias | Snapshots | Key-value dictionary snapshot holding named element states.                  |
| `SnapshotDiffItem`  | TypeAlias | Snapshots | Triplet `(element_path, old_value, new_value)` recording a single state diff.|
| `SnapshotDiffTuple` | TypeAlias | Snapshots | Tuple holding multiple state difference items for change tracking.          |
| `SnapshotTuple`     | TypeAlias | Snapshots | Immutable sequence tuple capturing raw values across composite elements.     |
| `StateDict`         | TypeAlias | State     | Key-value dictionary storing flat serialized attribute state values.         |
| `ValidTypes`        | TypeAlias | Types     | Type contract accepting standard Python types or union type annotations.     |
"""