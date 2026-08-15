from .core_mixins import (
    Infrastructure,
    NodesDicts,
    NodesTuple,
    Serialization,
    Snapshot,
)

from .dunders.collections import CollectionBase, Iterable, Mapping, Collection
from .dunders.comparison import Equality, Ordering
from .dunders.generics import ClassGetItem
from .dunders.interfaces import Call, ContextManager
from .dunders.lifecycles import Copyable, PickleState, PicleReduce, Lifecycle
from .dunders.numeric import Arithmetic, Bitwise, Conversion, Inplace, Unary
from .dunders.representation import ValueDisplay, ValueFormatting

from .others.immutable import ImmutableMethods, ImmutableWithInners
from .others.numerical import Equalizer, Volume
from .others.properties import InnersProperty, MetaShortcuts
from .others.state import DefaultState, DirtyTracking, History, Permission


__all__ = [
    # core_mixins
    "Infrastructure",
    "NodesDicts",
    "NodesTuple",
    "Serialization",
    "Snapshot",
    # dunders.collections
    "CollectionBase",
    "Iterable",
    "Mapping",
    "Collection",
    # dunders.comparison
    "Equality",
    "Ordering",
    # dunders.generics
    "ClassGetItem",
    # dunders.interfaces
    "Call",
    "ContextManager",
    # dunders.lifecycles
    "Copyable",
    "PickleState",
    "PicleReduce",
    "Lifecycle",
    # dunders.numeric
    "Arithmetic",
    "Bitwise",
    "Conversion",
    "Inplace",
    "Unary",
    # dunders.representation
    "ValueDisplay",
    "ValueFormatting",
    # others.immutable
    "ImmutableMethods",
    "ImmutableWithInners",
    # others.numerical
    "Equalizer",
    "Volume",
    # others.properties
    "InnersProperty",
    "MetaShortcuts",
    # others.state
    "DefaultState",
    "DirtyTracking",
    "History",
    "Permission",
]


_DESIGN_NOTES = """
# Mixins Package Overview

The `mixins` package is the public entry point for the entire Simple
mixin ecosystem. It propagates every mixin from every sub-package —
`core_mixins`, `dunders`, and `others` — so any mixin can be imported
directly from `simplibs.object.mixins` rather than reaching into a
specific sub-package.

## Sub-Packages

| Sub-package    | Type      | Description                                                    |
| :-------------- | :--------- | :----------------------------------------------------------------- |
| `core_mixins`     | Foundation | Node-tree walking, snapshotting, serialization — shared by both. |
| `dunders`          | Category   | Mixins implementing standard Python dunder protocols.             |
| `others`            | Category   | Mixins adding Simple-ecosystem-specific behavior.                 |

## Notes
- This is the only `__init__.py` in the package that defines `__all__`
  or re-exports across sub-package boundaries — every inner `__init__.py`
  (including `dunders/__init__.py` and `others/__init__.py`) is scoped to
  its own folder and does not propagate further.
- `core_mixins` is exposed at the top level alongside `dunders` and
  `others`, reflecting that it is shared infrastructure rather than a
  sibling category of either.
"""
