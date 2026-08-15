from .Infrastructure import Infrastructure
from .NodesDicts import NodesDicts
from .NodesTuple import NodesTuple
from .Serialization import Serialization
from .Snapshot import Snapshot


_DESIGN_NOTES = """
# Core Mixins

## Purpose
Shared infrastructure used throughout the mixin ecosystem for walking an
instance's node tree, snapshotting its state, and serializing it. Every
mixin in `dunders` and `others` that needs to read/restore/compare state
is ultimately built on top of one of these.

## Components

| Component          | Type  | Description                                                    |
| :----------------- | :---- | :--------------------------------------------------------------- |
| `NodesTuple`       | Mixin | Builds `_nodes_tuple`, the flat ordered source of every node.    |
| `NodesDicts`       | Mixin | Turns `_nodes_tuple` into fast name-keyed lookup dicts.          |
| `Snapshot`         | Mixin | Builds, restores, and compares full-state value tuples.          |
| `Infrastructure`   | Mixin | Bundles `NodesDicts` + `Snapshot` into one shared foundation.    |
| `Serialization`    | Mixin | Full `to_dict`/`to_json`/`from_dict`/`from_json` API.            |

## Notes
- Dependency order: `NodesTuple` → `NodesDicts` / `Snapshot` →
  `Infrastructure` → `Serialization`.
- `Infrastructure` is the base class most higher-level mixins should
  inherit from when they need both node lookup and snapshot access.
"""
