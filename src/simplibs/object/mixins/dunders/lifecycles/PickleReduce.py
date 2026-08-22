from typing import TYPE_CHECKING
# Inners
from .PickleState import PickleState
from ._utils import rebuild_simple_instance
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.lifecycles import PickleReduceProtocol
    from ...._core.protocols.mixins.dunders.lifecycles.internal_types import PicklePlan


class PickleReduce(PickleState):
    """
    Provides an implementation of the pickle protocol (__reduce__).

    Logic:
    - Callable = rebuild_simple_instance helper function
    - Arguments = (owner_class, mixins, is_constant, is_mutable, state)

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
        - callable: top-level helper rebuild_simple_instance
        - args: configuration tuple required to reconstruct mutable/immutable instance
        """
        return (
            rebuild_simple_instance,
            (
                self.meta.owner_class,
                self.__mixins__,
                self.__is_constant__,
                self.__is_mutable__,
                self.__getstate__(),
            ),
        )


_DESIGN_NOTES = """
# PickleReduce

## Purpose
Implements `__reduce__`, the top-level hook `pickle` calls first to learn
how to reconstruct an object: what callable to invoke and what arguments
to pass it.

## Compatibility
- No compatibility flags. Inherits from `PickleState` specifically to
  reuse its `__getstate__` implementation — this mixin adds the
  `__reduce__` layer on top rather than duplicating state logic.

## Logic
`__reduce__` returns a 2-tuple:
1. `rebuild_simple_instance` — static, module-level factory function capable of
   rebuilding dynamically compiled instance classes.
2. `(owner_class, mixins, is_constant, is_mutable, state)` — tuple of parameters
   and the saved state produced by `PickleState` via `to_dict()`.

This design guarantees seamless unpickling for both mutable and immutable instances
without relying on in-place `__setstate__` side effects from Python's standard
deserializer.

## Notes
- To customize pickling behavior, override `__getstate__` in a mixin
  placed above this one in the MRO — `__reduce__` itself rarely needs to
  change.
"""