from .NodesDicts import NodesDicts
from .Snapshot import Snapshot


class Infrastructure(NodesDicts, Snapshot):
    """
    Shared infrastructural foundation (nodes and snapshots) required for
    immutability logic, serialization, and reactive invocation.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()


_DESIGN_NOTES = """
# Infrastructure

## Purpose
Convenience "bundle" mixin — combines `NodesDicts` and `Snapshot` into a
single shared foundation, so any mixin that needs both node-lookup
(dicts by name) and snapshot-based state (build/restore/compare) can
inherit from one place instead of listing both parents itself.

## Compatibility
- No compatibility flags — inherits whatever its parents declare.
  Neither `NodesDicts` nor `Snapshot` restrict atom/composite or mutable/
  immutable on their own; the restriction (if any) belongs to the
  higher-level mixin that actually uses this foundation.

## Composition
Adds no logic of its own. `NodesDicts` supplies name-keyed lookup
dictionaries (`_nodes_dict`, `_nodes_instance_dict`, ...), and `Snapshot`
(via `NodesTuple`) supplies the ordered `_nodes_tuple` plus
build/restore/compare methods. Both ultimately share the same
`_nodes_tuple` source of truth, so combining them here avoids building it
twice.

## Notes
- This is the base class for `Serialization`, `ImmutableMethods`, and
  every other mixin in the ecosystem that needs to walk or snapshot the
  instance's node tree — it is rarely used directly on its own.
- Mirrors the "main/" bundling pattern seen in the dunders package
  (`Collection`, `Lifecycle`), just without a dedicated `main/`
  subfolder since it lives at the top of the `core_mixins` hierarchy.
"""
