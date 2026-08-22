from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.state import PermissionProtocol


class Permission(SimpleMixin):
    """
    Read-only mode — locking against changes.

    Example:
        obj.lock()
        obj.value = 10  # → ValueError
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _mutable_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def is_locked(
        self: "PermissionProtocol"
    ) -> bool:
        """Returns a bool indicating whether the lock is active."""
        return self._locked

    # ----------------------------------------
    # Methods - LOCK / UNLOCK
    # ----------------------------------------

    def lock(
        self: "PermissionProtocol"
    ) -> None:
        """Engages the lock."""
        object.__setattr__(self, "_locked", True)

    def unlock(
        self: "PermissionProtocol"
    ) -> None:
        """Releases the lock."""
        object.__setattr__(self, "_locked", False)


_DESIGN_NOTES = """
# Permission

## Purpose
Gives a mutable instance a runtime read-only switch — `obj.lock()` turns
further writes into errors, `obj.unlock()` turns them back on. Useful for
temporarily protecting a mutable instance without converting it to an
actual immutable class.

> For newcomers: this is different from immutability by design (the
> `_immutable_only` mixins) — that's a permanent, structural property of
> the class. `Permission` is a *runtime* toggle on an otherwise mutable
> instance, checked at write time rather than baked into the class.

## Compatibility
- `_mutable_only = True` — locking only makes sense where writes are
  otherwise allowed; an immutable instance already rejects all writes
  unconditionally, so this mixin would be redundant there.

## Logic
- `is_locked` simply exposes the internal `_locked` flag.
- `lock()` / `unlock()` set `_locked` via `object.__setattr__` rather
  than plain attribute assignment — bypassing any custom `__setattr__`
  the instance class might define, since the lock flag itself must
  always be settable even while the instance is otherwise locked.

## Notes
- `_locked` is not initialized by this mixin's `init_mixins` — in fact
  this mixin doesn't override `init_mixins` at all. The attribute is
  defined directly on every atomic instance by `create_atom_init`
  (`self._locked = False`), and the check for it lives directly inside
  `create_value_setter` (`if self._locked: raise_locked_value_error(...)`).
  In other words: every instance already carries `_locked` and already
  enforces it, purely as part of how atomic instances and their value
  setters are built — not as something this mixin sets up.
- `Permission` therefore adds **no new mechanism** — it only exposes a
  friendly public API (`lock()`, `unlock()`, `is_locked`) over
  infrastructure that already exists on every instance regardless of
  whether this mixin is used. This was a deliberate choice: building a
  separate access path into the value setter just for this one mixin
  would have added complexity for a single consumer, so `_locked` was
  folded directly into the shared atomic-instance construction instead.
- A practical consequence: even instances that don't use `Permission`
  still carry a (permanently `False`) `_locked` attribute and pay the
  cost of the `if self._locked:` check on every value write. This mixin
  is what turns that otherwise-dormant flag into a usable feature.
"""
