# Inners
from ..Iterable import Iterable
from ..Mapping import Mapping


class Collection(Iterable, Mapping):
    """
    Complete collection behavior for composite instances.
    Combines both iteration and dict-like API.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _composite_only = True

    # Slot definition
    __slots__ = ()


_DESIGN_NOTES = """
# Collection

## Purpose
Convenience "bundle" mixin — combines `Iterable` and `Mapping` into a
single mixin so a composite instance can behave like a full read-mostly
mapping (iteration, `len()`, `in`, `obj[key]`, `keys()`/`values()`/
`items()`) without listing both mixins separately every time.

## Compatibility
- `_composite_only = True` — inherited requirement from both parents;
  restated here for visibility.

## Composition
Adds no logic of its own. Its only job is the MRO: `Iterable` and
`Mapping` both build on `CollectionBase`, so combining them here gives one
shared `_inners_name_tuple` / `_inners_name_set` pair instead of two.

## Notes
- Use this instead of `Iterable` + `Mapping` whenever a composite needs
  the full dict-like surface; use the individual mixins when only part of
  that surface makes sense (e.g. iteration without item assignment).
- Mirrors the `Lifecycle` mixin's "main/" composition pattern used
  elsewhere in `dunders/`.
"""
