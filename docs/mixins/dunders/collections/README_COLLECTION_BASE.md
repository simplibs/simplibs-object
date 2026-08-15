from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders import CollectionBaseProtocol
    from ...._core.protocols.alias_typings import NamesSet, NamesTuple


class CollectionBase(SimpleMixin):
    """
    Base mapping mixin for composite instances.
    Builds a frozen mapping {name_snake: inner_instance} and provides
    the basic keys(), values(), items() API.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _composite_only = True

    # Slot definition
    __slots__ = ("_inners_name_set", "_inners_name_tuple")

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "CollectionBaseProtocol"
    ) -> None:
        """
        Initializes two immutable structures for working with inners:

        - `_inners_name_tuple`: tuple of all name_snake keys in the
          deterministic order defined by the blueprint. Serves as the
          source for iteration, reversed(), keys(), values() and items().

        - `_inners_name_set`: set of all name_snake keys. Used for fast
          existence checks (O(1) lookup).

        Both structures are derived only from direct inners and are
        immutable for the entire lifetime of the instance.
        """

        # 1. Initialize parents
        super().init_mixins()

        # 2. Tuple holding name_snake in exact order
        self._inners_name_tuple: "NamesTuple" = tuple(
            inner.meta.name_snake
            for inner in self.meta.inners
        )

        # 3. Set for fast presence comparison
        self._inners_name_set: "NamesSet" = set(self._inners_name_tuple)

    # ----------------------------------------
    # Methods - KEYS / VALUES / ITEMS
    # ----------------------------------------

    def keys(
        self: "CollectionBaseProtocol"
    ) -> list[str]:
        """Returns a list of keys (name_snake) of all direct inners."""
        return list(self._inners_name_tuple)

    def values(
        self: "CollectionBaseProtocol"
    ) -> list[object]:
        """Returns a list of values corresponding to each inner."""
        return [
            getattr(self, key)
            for key in self._inners_name_tuple
        ]

    def items(
        self: "CollectionBaseProtocol"
    ) -> list[tuple[str, object]]:
        """Returns a list of (key, value) pairs for all inners."""
        return [
            (key, getattr(self, key))
            for key in self._inners_name_tuple
        ]


_DESIGN_NOTES = """
# CollectionBase

## Purpose
Gives a composite instance basic "mapping" behavior — it starts to feel a
little like a read-only dict. Provides `keys()`, `values()`, `items()` over
the instance's direct inners (the parts it's composed of).

> For newcomers: a composite instance (e.g. `Person` made of `FirstName`
> and `LastName`) holds its inners as attributes. This mixin builds a
> familiar dict-like surface on top, so callers don't have to walk
> attributes manually.

## Compatibility
- `_composite_only = True` — only makes sense for composites. An atomic
  `SimpleConstant` has no inners, so there is nothing to map.

## Logic
On `init_mixins`, the mixin computes and freezes two derived structures
once:

- `_inners_name_tuple` — ordered keys (`name_snake`), matching the
  blueprint definition order. Source of truth for iteration and for the
  order returned by `keys()` / `values()` / `items()`.
- `_inners_name_set` — same keys as a set, for O(1) membership checks
  instead of a linear scan through the tuple.

Both are derived from direct inners only (not nested/deeper levels) and
never change again during the instance's lifetime — a one-time
computation, not something recalculated on every call.

> Why two structures for essentially the same data? The tuple is cheap to
> iterate and preserves order; the set is more expensive to build but
> cheap to query. The mixin trades a little memory for speed on both
> fronts.

## Notes
- `keys()`, `values()`, `items()` return fresh `list` objects, not views
  like `dict` does — every call is a new copy.
- This is not a full `Mapping` (no `__getitem__`, `__len__`, `__iter__`,
  etc.) — deliberately a minimal API, not a `dict` replacement. See
  `Mapping` and `Iterable` for the rest.
"""
