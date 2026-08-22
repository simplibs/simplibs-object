from typing import TYPE_CHECKING
from types import MappingProxyType
# Inners
from .NodesTuple import NodesTuple
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.core_mixins import NodesDictsProtocol
    from ..._core.protocols.alias_typings import NodesDict, NodesInstanceDict, NodesPathDict, NodesIndexMap


class NodesDicts(NodesTuple):
    """
    Provides serialization of the instance into dict/JSON and restoration
    from them. Foundation for HistoryMixin.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = (
        "_nodes_dict",
        "_nodes_instance_dict",
        "_nodes_path_dict",
        "_nodes_index_map"
    )

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "NodesDictsProtocol"
    ) -> None:
        """
        Method forwarding its logic into the instance's initialization
        process.
        """

        # 1. Base immutable dict for name_snake-based access to nodes_tuple values
        self._nodes_dict: "NodesDict" = MappingProxyType({
            instance.meta.name_snake: (instance, path)
            for instance, path in self._nodes_tuple
        })

        # 2. Immutable dict for name_snake-based access to the instance
        self._nodes_instance_dict: "NodesInstanceDict" = MappingProxyType({
            instance.meta.name_snake: instance
            for instance, _ in self._nodes_tuple
        })

        # 3. Immutable dict for name_snake-based access to the path
        self._nodes_path_dict: "NodesPathDict" = MappingProxyType({
            instance.meta.name_snake: path
            for instance, path in self._nodes_tuple
        })

        # 4. Immutable dict for index-based access to nodes_tuple items
        self._nodes_index_map: "NodesIndexMap" = MappingProxyType({
            instance.meta.name_snake: index
            for index, (instance, _) in enumerate(self._nodes_tuple)
        })


_DESIGN_NOTES = """
# NodesDicts

## Purpose
Turns the ordered `_nodes_tuple` from `NodesTuple` into fast, name-keyed
lookup structures — so instead of scanning the tuple linearly to find a
node by name, mixins can do a direct dict lookup (O(1)).

> For newcomers: `_nodes_tuple` answers "give me everything in order";
> `NodesDicts` answers "give me the thing called X" — same underlying
> data, different access pattern.

## Compatibility
- No compatibility flags — inherited from `NodesTuple`, works for both
  atoms and composites.

## Logic
On `init_mixins`, four `MappingProxyType` (read-only) dicts are built
from `_nodes_tuple`, all keyed by `instance.meta.name_snake`:

- `_nodes_dict` — name → `(instance, path)`, the full pair.
- `_nodes_instance_dict` — name → `instance` only.
- `_nodes_path_dict` — name → `path` only.
- `_nodes_index_map` — name → its position (index) in `_nodes_tuple`.

Each is a different "view" of the same source data, tailored to whichever
lookup a caller needs, without forcing every caller to unpack the full
pair every time.

## Notes
- All four dicts use `MappingProxyType`, making them genuinely read-only
  at the Python level — not just "please don't mutate this," but
  enforced immutability of the mapping itself, even though the instance
  as a whole may still be mutable.
- Every dict is rebuilt fully at `init_mixins` time and never touched
  again — like `CollectionBase` in the dunders package, this is a
  one-time computation, not a cache that gets invalidated later.
"""
