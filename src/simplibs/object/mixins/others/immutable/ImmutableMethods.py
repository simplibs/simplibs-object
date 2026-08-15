from typing import Any, TYPE_CHECKING
# Outers
from ...core_mixins import Infrastructure
from ..._common_logic.immutability import (
    with_constants,
    with_constant,
    with_composite,
    with_any,
    create_new_instance
)
# Inners
from ._validations import raise_with_changes_input_not_dict
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.immutable import ImmutableMethodsProtocol
    from ...._core.protocols.alias_typings import ChangesTuple, ChangesDict


class ImmutableMethods(Infrastructure):
    """
    Mixin providing the immutable API for working with instances:

    - with_constants(...)
    - with_constant(...)
    - with_composite(...)

    Construction of immutable classes (getter-only value, removal of
    setters, removal of mutating methods, immutable inners) is now
    handled directly in make_atom_class / make_composite_class.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _immutable_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - Immutable API (core)
    # ----------------------------------------

    def with_constants(
        self: "ImmutableMethodsProtocol",
        changes_tuple: "ChangesTuple | None" = None
    ) -> "ImmutableMethodsProtocol":
        """Creates a new immutable instance based on multiple changes."""
        return with_constants(self, changes_tuple)

    def with_constant(
        self: "ImmutableMethodsProtocol",
        name: str,
        new_value: Any
    ) -> "ImmutableMethodsProtocol":
        """Creates a new immutable instance by changing a single constant."""
        return with_constant(self, name, new_value)

    def with_composite(
        self: "ImmutableMethodsProtocol",
        name: str,
        new_value: Any
    ) -> "ImmutableMethodsProtocol":
        """Creates a new immutable instance by changing a single composite."""
        return with_composite(self, name, new_value)

    # ----------------------------------------
    # Methods - Immutable API (extended)
    # ----------------------------------------

    def with_changes(
        self: "ImmutableMethodsProtocol",
        changes_dict: "ChangesDict"
    ) -> "ImmutableMethodsProtocol":
        """Method allowing multiple constant changes to be given as a dict."""
        if not isinstance(changes_dict, dict):
            raise_with_changes_input_not_dict(self, changes_dict)
        return with_any(self, tuple(changes_dict.items()))

    def with_value(
        self: "ImmutableMethodsProtocol",
        new_value: Any
    ) -> "ImmutableMethodsProtocol":
        """Method for changing the main value - a convenience alias."""
        return self.with_composite(self.meta.name_snake, new_value)

    def duplicate(
        self: "ImmutableMethodsProtocol"
    ) -> "ImmutableMethodsProtocol":
        """Method returning a new instance with the same values."""
        return create_new_instance(self, self._build_snapshot())


_DESIGN_NOTES = """
# ImmutableMethods

## Purpose
The core "change without mutating" API for immutable instances —
`with_constant`, `with_composite`, `with_constants`, plus the more
ergonomic `with_changes` (dict-based) and `with_value` (alias for
changing the top-level value) and `duplicate` (identical copy).

> For newcomers: this is the classic immutable-object pattern — instead
> of `obj.value = 10`, you write `new_obj = obj.with_value(10)` and the
> original `obj` is left untouched. Every method here returns a new
> instance rather than modifying `self`.

## Compatibility
- `_immutable_only = True` — the whole premise of "return a new
  instance instead of mutating" only makes sense for immutable objects;
  mutable instances get their equivalent API elsewhere (direct attribute
  assignment, or the `Call`/`Inplace` dunder mixins).

## Logic
- The three "core" methods (`with_constants`, `with_constant`,
  `with_composite`) are thin wrappers delegating straight to the
  matching top-level utility functions — this class adds no logic beyond
  routing.
- `with_changes(changes_dict)` validates the input is actually a `dict`
  (raising a descriptive error via `raise_with_changes_input_not_dict`
  otherwise), then converts it to the tuple-of-pairs shape `with_any`
  expects.
- `with_value(new_value)` is sugar for
  `self.with_composite(self.meta.name_snake, new_value)` — i.e. "change
  the value this instance itself represents," using its own name as the
  composite key.
- `duplicate()` builds a snapshot of the current state and feeds it into
  `create_new_instance` — producing an equal-but-distinct instance
  without going through any change logic at all.

## Notes
- The docstring's mention that immutable class construction (getter-only
  values, no setters) happens in `make_atom_class`/`make_composite_class`
  is a pointer to *where else* to look — this mixin only supplies the
  "change" API, not the structural immutability itself.
- `duplicate()` is functionally similar to `Copyable.__copy__` in the
  dunders package — both build from a snapshot — but is exposed here as
  a named, discoverable method rather than only reachable via
  `copy.copy()`.
"""
