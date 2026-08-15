from typing import TYPE_CHECKING
# Outers
from ...core_mixins import Snapshot
from ..._common_logic.immutability import create_new_instance
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.state import DefaultStateProtocol
    from ...._core.protocols.alias_typings import SnapshotTuple


# noinspection PyProtectedMember
class DefaultState(Snapshot):
    """
    Mixin providing the instance with:
    - a stored default state (_default_state)
    - the methods clone_instance(), reset_to_default_values(),
      create_new_default_instance()
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _mutable_only = True

    # Slot definition
    __slots__ = ("_default_state_snapshot",)

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "DefaultStateProtocol"
    ) -> None:
        """
        Method forwarding its logic into the instance's initialization
        process.
        """

        # 1. Initialize parents
        super().init_mixins()

        # 2. Build a snapshot of the default state
        self._default_state_snapshot: "SnapshotTuple" = self._build_snapshot()

    # ----------------------------------------
    # Methods - CLONE / RESET / NEW
    # ----------------------------------------

    def clone_instance(
        self: "DefaultStateProtocol"
    ) -> "DefaultStateProtocol":
        """Creates a new instance with the same state as this instance."""
        new_instance = self.create_new_default_instance()
        new_instance._restore_snapshot(self._build_snapshot())
        return new_instance

    def reset_to_default_values(
        self: "DefaultStateProtocol"
    ) -> None:
        """Resets the instance to its default state (_default_state)."""
        self._restore_snapshot(self._default_state_snapshot)

    # noinspection PyTypeChecker
    def create_new_default_instance(
        self: "DefaultStateProtocol"
    ) -> "DefaultStateProtocol":
        """
        Returns a new instance of the same type, with the same default
        state this instance had when it was created.
        """
        return create_new_instance(self, self._default_state_snapshot)


_DESIGN_NOTES = """
# DefaultState

## Purpose
Remembers the state a mutable instance was created with, and provides
three ways to use that memory: `reset_to_default_values()` (go back to
it), `create_new_default_instance()` (build a fresh instance starting
from it), and `clone_instance()` (build a new instance matching the
*current* state).

> For newcomers: "default state" here means "what this specific instance
> looked like at construction time" — not the blueprint's class-level
> defaults. Two instances of the same class, created with different
> initial values, will each remember their own default state.

## Compatibility
- `_mutable_only = True` — resetting/restoring in place only makes sense
  for mutable instances; an immutable instance can't have its state
  overwritten regardless.

## Logic
- On `init_mixins`, `_default_state_snapshot` is captured once, right
  after construction — this becomes the fixed reference point for the
  rest of the instance's life.
- `reset_to_default_values()` simply restores that snapshot via
  `_restore_snapshot`, discarding any changes made since creation.
- `create_new_default_instance()` builds a brand-new instance using
  `create_new_instance` seeded with `_default_state_snapshot` — the
  result reflects where *this* instance started, not where it is now.
- `clone_instance()` combines both ideas: it first creates a fresh
  default instance via `create_new_default_instance()`, then immediately
  overwrites it with a snapshot of the *current* state via
  `_restore_snapshot`. The two-step approach (build clean, then restore
  current) reuses the default-instance construction path rather than
  duplicating instance-creation logic for the "clone" case.

## Notes
- Compare with `DirtyTracking`, which answers "has this changed since a
  reference point" — `DefaultState` instead answers "let me get back to
  or start fresh from that reference point." The two mixins share the
  same snapshot foundation but serve different questions.
- `clone_instance()`'s two-step build is worth noting for anyone
  debugging performance — it constructs a full default instance as an
  intermediate step, even though only the final restored state is kept.
"""
