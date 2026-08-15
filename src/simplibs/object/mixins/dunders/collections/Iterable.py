from typing import TYPE_CHECKING
from collections.abc import Iterator
# Inners
from .CollectionBase import CollectionBase
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.collections import IterableProtocol


class Iterable(CollectionBase):
    """
    Iteration API for composite instances.
    Enables iteration, reverse iteration, and an extended dir() listing.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _composite_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - ITER / REVERSED / DIR
    # ----------------------------------------

    def __iter__(
        self: "IterableProtocol"
    ) -> Iterator[str]:
        """Iterates over the keys (name_snake) of all inners in defined order."""
        return iter(self._inners_name_tuple)

    def __reversed__(
        self: "IterableProtocol"
    ) -> Iterator[str]:
        """Returns a reverse iterator over the inner keys."""
        return reversed(self._inners_name_tuple)

    def __dir__(
        self: "IterableProtocol"
    ) -> list[str]:
        """Extends the attribute listing with the inner keys."""
        base = list(object.__dir__(self))
        base += list(self._inners_name_tuple)
        return sorted(set(base))


_DESIGN_NOTES = """
# Iterable

## Purpose
Makes a composite instance iterable the way Python programmers expect:
`for key in person`, `reversed(person)`, and a `dir(person)` that also
shows the inner names — useful in a REPL or debugger.

> Note the iteration is over *keys* (name_snake), not values — mirroring
> how `for x in some_dict` iterates over dict keys, not items.

## Compatibility
- `_composite_only = True` — builds directly on `CollectionBase`'s
  `_inners_name_tuple`, which only exists for composites.

## Logic
All three dunders are thin wrappers around the tuple already frozen by
`CollectionBase.init_mixins`:

- `__iter__` / `__reversed__` just forward to `iter()` / `reversed()` on
  that tuple — no extra computation.
- `__dir__` merges the default `object.__dir__(self)` listing with the
  inner keys, so autocomplete and `dir()` reveal the composite's
  structure, not just its methods.

## Notes
- Combine with `Mapping` (see `Collection`) to get `obj[key]` access on
  top of the keys this mixin lets you iterate.
- Inherits `_composite_only` from `CollectionBase` — declared again here
  for clarity, not because the value changes.
"""
