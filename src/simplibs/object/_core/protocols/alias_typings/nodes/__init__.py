from .NodeItem import NodeItem
from .NodesDict import NodesDict
from .NodesIndexMap import NodesIndexMap
from .NodesInstanceDict import NodesInstanceDict
from .NodesPathDict import NodesPathDict
from .NodesTuple import NodesTuple

_DESIGN_NOTES = """
# Nodes Alias Typings Sub-Package

## Purpose
Provides type definitions for hierarchy node registries, positional indexing, path mapping, and live instance lookup.

## Internal Components Registry

| Component           | Type      | Description                                                                  |
| :------------------ | :-------- | :--------------------------------------------------------------------------- |
| `NodeItem`          | TypeAlias | Pair structure `(live_instance, path_tuple)` representing a registered node. |
| `NodesDict`         | TypeAlias | Complex map associating node names with their `(instance, path)` pair.       |
| `NodesIndexMap`     | TypeAlias | Sequence index map storing original positional offsets for subnodes.          |
| `NodesInstanceDict` | TypeAlias | Direct lookup mapping snake_case names directly to live instances.           |
| `NodesPathDict`     | TypeAlias | Path mapping associating subnode names with their hierarchical path tuples.  |
| `NodesTuple`        | TypeAlias | Ordered sequence tuple holding all node items in a composite structure.      |
"""