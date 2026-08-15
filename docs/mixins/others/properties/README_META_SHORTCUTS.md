from typing import TYPE_CHECKING, Any
# Outers
from ..base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.instance import SimpleInstanceLike
    from ...._core.protocols.alias_typings import ValidTypes


class MetaShortcuts(SimpleMixin):
    """
    Ergonomic shortcuts for frequently used items from the object's
    metadata. Adds no logic of its own — it only exposes selected
    information directly on the instance.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # -------------------------
    # Property - Object identity
    # -------------------------
    @property
    def name_snake(
        self: "SimpleInstanceLike"
    ) -> str:
        """Snake_case name of the object's class."""
        return self.meta.name_snake

    # -------------------------
    # Property - Type information
    # -------------------------
    @property
    def value_type(
        self: "SimpleInstanceLike"
    ) -> ValidTypes:
        """The Python type of the value the object holds."""
        return self.meta.value_type

    @property
    def default(
        self: "SimpleInstanceLike"
    ) -> Any:
        """The object's default value, as defined in its metadata."""
        return self.meta.default

    # -------------------------
    # Property - Object structure
    # -------------------------
    @property
    def is_atom(
        self: "SimpleInstanceLike"
    ) -> bool:
        """True if the object represents an atom (has no inners)."""
        return self.meta.is_constant

    @property
    def is_composite(
        self: "SimpleInstanceLike"
    ) -> bool:
        """True if the object represents a composite (has inners)."""
        return not self.meta.is_constant

    @property
    def is_decomposeable(
        self: "SimpleInstanceLike"
    ) -> bool:
        """True if the object's value can be changed via decomposition."""
        return getattr(self.meta, "is_decomposeable", False)


_DESIGN_NOTES = """
# MetaShortcuts

## Purpose
Pure convenience mixin — pulls a handful of frequently-needed facts out
of `self.meta` and exposes them as top-level properties on the instance,
so callers can write `obj.is_atom` instead of `obj.meta.is_constant`.

> For newcomers: this mixin is a good example of a mixin that adds zero
> new behavior — every property is a direct, one-line pass-through to an
> existing `meta` attribute. Its entire value is ergonomics: shorter,
> more discoverable names on the object people actually interact with.

## Compatibility
- No compatibility flags — every property reads from `self.meta`, which
  every Simple instance has regardless of atom/composite or mutable/
  immutable status.

## Logic
Grouped into three small clusters, each a direct pass-through:
- **Identity**: `name_snake` → `meta.name_snake`.
- **Type info**: `value_type` → `meta.value_type`, `default` →
  `meta.default`.
- **Structure**: `is_atom` → `meta.is_constant`; `is_composite` is
  defined as its logical negation rather than a separate stored flag, so
  the two can never disagree; `is_decomposeable` uses `getattr(...,
  False)` rather than a direct attribute access, tolerating metadata
  objects that don't define this optional flag at all.

## Notes
- `is_composite` deliberately isn't `self.meta.is_composite` — computing
  it as `not self.meta.is_constant` keeps a single source of truth
  (`is_constant`) instead of two flags that could drift out of sync.
- `is_decomposeable`'s defensive `getattr` fallback is the one spot in
  this mixin that isn't a pure 1:1 passthrough — worth knowing if a
  future metadata refactor makes the field mandatory, since the fallback
  would then be silently redundant rather than protective.
"""
