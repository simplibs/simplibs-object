from typing import Any, TYPE_CHECKING
import copy as _copy
# Outers
from ...core_mixins import NodesDicts, Snapshot
from ..._common_logic.immutability import create_new_instance
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.lifecycles import CopyableProtocol


class Copyable(NodesDicts, Snapshot):
    """
    Shared mixin for both mutable and immutable variants.

    Mutable lifecycle:
    - shallow copy via create_instance(validate=False)
    - deep copy via create_instance(validate=False)

    Immutable lifecycle:
    - shallow copy via snapshot
    - deep copy via deepcopy of the snapshot
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - COPY / DEEPCOPY
    # ----------------------------------------

    def __copy__(
        self: "CopyableProtocol"
    ) -> "CopyableProtocol":
        """
        Creates and returns a shallow copy of this instance.
        Reacts safely to the object's mutable/immutable mode.
        """

        # 1. Build a snapshot
        snapshot = self._build_snapshot()

        # 2. Build and return the new instance
        return create_new_instance(self, snapshot)

    def __deepcopy__(
        self: "CopyableProtocol",
        memo: dict[int, Any]
    ) -> "CopyableProtocol":
        """
        Creates and returns a deep copy of this instance.
        The `memo` dict is used internally to track already-visited
        objects, to avoid infinite recursion on cycles.
        """

        # 1. Build a snapshot
        snapshot = tuple(
            _copy.deepcopy(v, memo)
            for v in self._build_snapshot()
        )

        # 2. Build and return the new instance
        return create_new_instance(self, snapshot)


_DESIGN_NOTES = """
# Copyable

## Purpose
Implements Python's standard `copy.copy()` / `copy.deepcopy()` protocol
(`__copy__` / `__deepcopy__`) for Simple instances, so they interoperate
with the built-in `copy` module the same way any other Python object
would.

## Compatibility
- No compatibility flags — works for both mutable and immutable
  instances. The distinction between the two lifecycles isn't handled
  here directly; it's absorbed by `_build_snapshot()` and
  `create_new_instance()`, which already know how to build a correct copy
  for either mode.

## Logic
Both dunders follow the same two-step shape:
1. Build a snapshot of the current state via `_build_snapshot()`
   (inherited from `Snapshot`).
2. Feed that snapshot into `create_new_instance()` to produce the copy.

The only difference between shallow and deep copy is what happens to the
snapshot in between: `__deepcopy__` runs every value in the snapshot
through `copy.deepcopy(v, memo)` first, using the standard `memo` dict to
correctly handle shared references and cycles; `__copy__` uses the
snapshot as-is.

## Notes
- Depends on `NodesDicts` and `Snapshot` for `_build_snapshot()` — this
  mixin doesn't rebuild that logic itself, it only orchestrates it.
- Named `Copyable` at the mixin level, but combined with pickle support
  in the `Lifecycle` bundle mixin — the two protocols share the same
  snapshot-based foundation.
"""
