from typing import TYPE_CHECKING
# Outers
from ..base_class import SimpleMixin
from .._common_logic.constants import VALUE
# Inners
from ._utils.nodes_tuple import build_nodes_tuple
# Annotations
if TYPE_CHECKING:
    from ..._core.protocols.mixins.core_mixins import NodesTupleProtocol
    from ..._core.protocols.alias_typings import NamesTuple, NamesSet
    from ..._core.protocols.alias_typings import NodesTuple as _NodesTuple


class NodesTuple(SimpleMixin):
    """
    Provides serialization of the instance into dict/JSON and restoration
    from them. Foundation for HistoryMixin.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = (
        "_nodes_tuple",
        "_node_names_tuple",
        "_constant_names_set"
    )

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "NodesTupleProtocol"
    ) -> None:

        # 1. Initialize parents
        super().init_mixins()

        # 2. Base tuple with instance and path (main source of truth)
        self._nodes_tuple: "_NodesTuple" = build_nodes_tuple(self)

        # 3. Tuple with names in the same order as _nodes_tuple
        self._node_names_tuple: "NamesTuple" = tuple(
            instance.meta.name_snake
            for instance, _ in self._nodes_tuple
        )

        # 4. Tuple with constant names
        self._constant_names_set: "NamesSet" = {
            instance.meta.name_snake
            for instance, path in self._nodes_tuple
            if path[-1] is not VALUE
        }


_DESIGN_NOTES = """
# NodesTuple

## Purpose
Builds the single source of truth for "everything reachable inside this
instance" — a flat, ordered tuple of every node (atom or composite,
however deeply nested) paired with its access path. Every other
tree-walking mixin (`NodesDicts`, `Snapshot`, `Equalizer`, `History`, ...)
is ultimately built on top of `_nodes_tuple`.

> For newcomers: think of `_nodes_tuple` as flattening the whole
> composite tree into a single list, so mixins that need to iterate
> "every value in this object" don't each have to walk the tree
> themselves.

## Compatibility
- No compatibility flags — meaningful for both atoms (a trivial
  single-node tuple) and composites (the full nested tree), since
  `build_nodes_tuple` handles both cases.

## Logic
On `init_mixins`, three structures are derived, in this order:
1. `_nodes_tuple` — built by `build_nodes_tuple(self)`; pairs of
   `(instance, path)` for every node, deterministic order.
2. `_node_names_tuple` — just the `name_snake` of each node, same order,
   for cheap name-based iteration without re-walking the tree.
3. `_constant_names_set` — a set of names whose path does *not* end in `VALUE`, 
   i.e. names that represent constants/atoms rather than the value slot of 
   a composite itself.
"""
