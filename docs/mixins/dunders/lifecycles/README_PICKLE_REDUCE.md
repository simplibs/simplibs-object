from typing import TYPE_CHECKING
# Inners
from .PickleState import PickleState
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.lifecycles import PickleReduceProtocol
    from ...._core.protocols.mixins.dunders.lifecycles.internal_types import PicklePlan


class PickleReduce(PickleState):
    """
    Provides an implementation of the pickle protocol (__reduce__).

    Logic:
    - Constructor = self.__class__
    - Arguments = ()
    - State = self.__getstate__()

    PickleState ensures __getstate__/__setstate__ work through
    to_dict/from_dict.

    This mixin inherits from PickleState so it has access to the default
    __getstate__ implementation, which relies on SerializationBase logic
    and its to_dict() method. If a user needs __getstate__ to work
    differently, they can simply override it with their own mixin, placed
    above this one in the MRO, replacing the original implementation.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - REDUCE
    # ----------------------------------------

    def __reduce__(
        self: "PickleReduceProtocol"
    ) -> "PicklePlan":
        """
        Pickle protocol:
        - callable: the instance's class
        - args: none (the class builds the instance itself)
        - state: the dict returned by __getstate__

        Note:
        - a mutable instance is built via create_instance through
          __class__()
        - an immutable instance is built as a snapshot-based instance via
          __setstate__
        """
        return (
            self.__class__,
            (),
            self.__getstate__()
        )


_DESIGN_NOTES = """
# PickleReduce

## Purpose
Implements `__reduce__`, the top-level hook `pickle` calls first to learn
how to reconstruct an object: what callable to invoke, what arguments to
pass it, and what state to apply afterward.

## Compatibility
- No compatibility flags. Inherits from `PickleState` specifically to
  reuse its `__getstate__` implementation — this mixin adds the
  `__reduce__` layer on top rather than duplicating state logic.

## Logic
`__reduce__` returns a fixed 3-tuple:
1. `self.__class__` — the callable pickle will call to rebuild the object.
2. `()` — no constructor arguments; the class is expected to be able to
   build a bare instance of itself.
3. `self.__getstate__()` — the actual saved state, produced by
   `PickleState` via `to_dict()`.

After unpickling, Python calls `__setstate__` with that state
automatically — which is where the mutable-vs-immutable branching
(mutate in place vs. return a new instance) actually happens, inside
`PickleState`, not here.

## Notes
- To customize pickling behavior, override `__getstate__` in a mixin
  placed above this one in the MRO — `__reduce__` itself rarely needs to
  change.
- Keeping `args` empty means the reconstructed instance always starts
  from a clean/default construction path before state is applied — this
  is a deliberate, not incidental, choice.
"""
