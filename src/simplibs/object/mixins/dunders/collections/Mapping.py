from typing import TYPE_CHECKING, Any
# Inners
from .CollectionBase import CollectionBase
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.collections import MappingProtocol


class Mapping(CollectionBase):
    """
    Dict-like API for composite instances.
    Provides access via obj[key], value assignment, and existence checks.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _composite_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - LEN / CONTAINS / MISSING
    # ----------------------------------------

    def __len__(
        self: "MappingProtocol"
    ) -> int:
        """Returns the number of direct inners."""
        return len(self._inners_name_tuple)

    def __contains__(
        self: "MappingProtocol",
        key: str
    ) -> bool:
        """Returns True if the composite contains an inner with the given key."""
        return key in self._inners_name_set

    def __missing__(
        self: "MappingProtocol",
        key: str
    ) -> None:
        """Raises KeyError with information about the available keys."""
        raise KeyError(
            f"Item '{key}' is not defined on {self.meta.class_name}. "
            f"Available items: {self.keys()}"
        )

    # ----------------------------------------
    # Methods - GETITEM / GET / SETITEM
    # ----------------------------------------

    def __getitem__(
        self: "MappingProtocol",
        key: str
    ):
        """Returns the value of an inner by key, or raises via __missing__."""
        if key not in self._inners_name_set:
            self.__missing__(key)
        return getattr(self, key)

    def get(
        self: "MappingProtocol",
        key: str,
        default: Any = None
    ):
        """Safely returns the value of an inner, or default if the key doesn't exist."""
        if key not in self._inners_name_set:
            return default
        return getattr(self, key)

    def __setitem__(
        self: "MappingProtocol",
        key: str,
        value: Any
    ):
        """Sets the value of an inner by key, if it exists."""

        # 1. Check that we are not on an immutable object
        if not self.__is_mutable__:
            raise TypeError(
                f"Immutable composite '{self.meta.class_name}' "
                f"does not allow changing values via __setitem__."
            )

        # 2. Check that the key exists
        if key not in self._inners_name_set:
            self.__missing__(key)

        # 3. Request the value change
        # (May be blocked on a composite without decomposition - an
        # exception is raised in that case)
        setattr(self, key, value)


_DESIGN_NOTES = """
# Mapping

## Purpose
Gives a composite instance `dict`-style item access: `obj[key]`,
`obj[key] = value`, `key in obj`, `obj.get(key, default)`, `len(obj)`.
Built on top of the same frozen key set `CollectionBase` already prepared.

## Compatibility
- `_composite_only = True` — items only exist on composites (inners).

## Logic
- `__len__` / `__contains__` are direct lookups against
  `_inners_name_tuple` / `_inners_name_set` — no extra work.
- `__getitem__` / `get()` both check key existence first; `__getitem__`
  delegates the "not found" case to `__missing__` (which raises a
  `KeyError` listing the available keys), while `get()` just returns the
  given `default` instead of raising.
- `__setitem__` is guarded by mutability: on an immutable composite it
  raises `TypeError` before even checking the key. On a mutable composite
  it validates the key, then delegates to `setattr`, which means the
  normal reactivity/validation pipeline for setting a value still runs —
  this mixin adds syntax, not a parallel write path.

## Notes
- `__missing__` is the single place that decides what "key not found"
  looks like — overriding just that method changes the error message
  everywhere without touching `__getitem__` itself.
- A composite without decomposition logic can still reject a `setattr`
  further down the pipeline — `__setitem__` only handles the
  mutability/key-existence checks that are its own responsibility.
- Pairs naturally with `Iterable`; together they form `Collection`.
"""
