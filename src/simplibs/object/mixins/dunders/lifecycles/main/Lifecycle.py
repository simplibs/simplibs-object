# Inners
from ..PickleReduce import PickleReduce
from ..Copyable import Copyable


class Lifecycle(Copyable, PickleReduce):
    """
    Provides a complete Lifecycle implementation by combining all the
    necessary mixins.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()


_DESIGN_NOTES = """
# Lifecycle

## Purpose
Convenience "bundle" mixin — combines `Copyable` and `PickleReduce` so an
instance gets full `copy`/`deepcopy`/`pickle` support from a single
mixin, instead of listing both separately.

## Compatibility
- No compatibility flags — inherited compatibility comes entirely from
  its two parents, both of which are themselves universal (mutable and
  immutable, atom and composite).

## Composition
Adds no logic of its own. `Copyable` supplies `__copy__`/`__deepcopy__`;
`PickleReduce` (via `PickleState`) supplies `__reduce__`/`__getstate__`/
`__setstate__`. Both ultimately rely on the same snapshot/serialization
foundation, so combining them here doesn't duplicate work — it just gives
one name to reach for both protocols together.

## Notes
- Mirrors the `Collection` mixin's "main/" bundling pattern used
  elsewhere in `dunders/`.
- Use the individual mixins (`Copyable`, `PickleReduce`) directly if an
  instance needs only one of the two protocols.
"""
