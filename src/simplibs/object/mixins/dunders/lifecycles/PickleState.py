from typing import TYPE_CHECKING
# Outers
from ...core_mixins import Serialization
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.lifecycles import PickleStateProtocol
    from ...._core.protocols.alias_typings import StateDict


class PickleState(Serialization):
    """
    Mixin providing pickle/unpickle behavior based on to_dict()/from_dict().

    This mixin implements the __getstate__ and __setstate__ dunders so
    that serialization happens through a readable dict (to_dict) and
    deserialization through the from_dict method. This keeps pickling
    stable, readable, and independent of the object's internal
    representation.

    Requirements:
    - The class MUST provide a from_dict() method (from
      MutableSerialization or ImmutableSerialization).
    - The mixin works both for mutable instances (in-place mutation) and
      immutable instances (from_dict returns a new instance, which pickle
      automatically uses).
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - GETSTATE / SETSTATE
    # ----------------------------------------

    def __getstate__(
        self: "PickleStateProtocol"
    ) -> "StateDict":
        """
        Returns the instance's state as a dict via to_dict().

        Pickle stores this dict as the object's representation. The
        benefit is that serialization is stable, readable, and
        independent of the instance's internal and private attributes.
        """
        return self.to_dict()

    def __setstate__(
        self: "PickleStateProtocol",
        state: "StateDict"
    ) -> None:
        """
        Restores the instance's state from a dict via from_dict().

        Checks whether the class provides a from_dict() method. If not,
        raises TypeError with a clear explanation. For mutable instances,
        the state is restored directly into self. For immutable
        instances, from_dict() returns a new instance, which pickle
        automatically uses as the resulting object.
        """
        if not hasattr(self.__class__, "from_dict"):
            raise TypeError(
                f"{self.__class__.__name__} requires a from_dict() method "
                f"(provided by MutableSerialization or ImmutableSerialization)."
            )

        self.from_dict(state)


_DESIGN_NOTES = """
# PickleState

## Purpose
Bridges the `pickle` module's `__getstate__`/`__setstate__` hooks to the
Simple ecosystem's own `to_dict()`/`from_dict()` serialization, so pickled
data is a readable dict rather than an opaque dump of internal attributes.

## Compatibility
- No compatibility flags, but has a hard runtime requirement: the class
  must provide `from_dict()` (supplied by `MutableSerialization` or
  `ImmutableSerialization`). Missing it raises a `TypeError` with a clear
  message rather than failing obscurely inside `pickle`.

## Logic
- `__getstate__` simply returns `self.to_dict()` — pickle stores that
  dict as the object's saved state.
- `__setstate__` first checks `from_dict` exists, then calls it with the
  restored dict:
  - **Mutable** instances apply the state in place onto `self`.
  - **Immutable** instances have `from_dict()` return a brand-new
    instance, which `pickle` transparently swaps in as the unpickled
    result — the caller never has to know this happened.

## Notes
- This mixin is the foundation `PickleReduce` builds on: it supplies
  `__getstate__`, which `PickleReduce.__reduce__` calls to fill the
  "state" slot of the pickle protocol.
- Overriding `__getstate__`/`__setstate__` in a mixin placed above this
  one in the MRO is the supported way to customize pickling without
  touching this file.
"""
