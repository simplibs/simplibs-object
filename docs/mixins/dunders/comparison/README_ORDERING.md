from typing import TYPE_CHECKING, Any
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.comparison import OrderingProtocol


# noinspection PyUnresolvedReferences
class Ordering(SimpleMixin):
    """
    Magnitude comparison for Simple instances.
    Compares by value (self.value).
    Works for comparing an instance against another instance or against
    a raw value.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - LT / LE / GT / GE
    # ----------------------------------------

    def __lt__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Returns True if this instance's value is less than the other
        operand's value. If the operand is a Simple instance, its .value
        is used; otherwise it is compared directly against the operand's
        value. Returns NotImplemented for incompatible types.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value < other_value
        except TypeError:
            return NotImplemented

    def __le__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Returns True if this instance's value is less than or equal to
        the other operand's value. If the operand is a Simple instance,
        its .value is used; otherwise it is compared directly against the
        operand's value. Returns NotImplemented for incompatible types.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value <= other_value
        except TypeError:
            return NotImplemented

    def __gt__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Returns True if this instance's value is greater than the other
        operand's value. If the operand is a Simple instance, its .value
        is used; otherwise it is compared directly against the operand's
        value. Returns NotImplemented for incompatible types.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value > other_value
        except TypeError:
            return NotImplemented

    def __ge__(
        self: "OrderingProtocol",
        other: Any
    ) -> bool:
        """
        Returns True if this instance's value is greater than or equal to
        the other operand's value. If the operand is a Simple instance,
        its .value is used; otherwise it is compared directly against the
        operand's value. Returns NotImplemented for incompatible types.
        """
        other_value = getattr(other, "value", other)
        try:
            return self.value >= other_value
        except TypeError:
            return NotImplemented


_DESIGN_NOTES = """
# Ordering

## Purpose
Adds `<`, `<=`, `>`, `>=` to a Simple instance, so instances can be
sorted, compared, and used with `min()`/`max()` the same way as the raw
values they wrap.

> Note this is a separate mixin from `Equality` — Python treats ordering
> and equality as independent concerns (a class can be equality-only, or
> support both). Splitting them lets a mixin combo opt into ordering only
> where it actually makes sense (e.g. numbers, dates) without forcing it
> onto every type (e.g. it rarely makes sense to order arbitrary
> composites).

## Compatibility
- No compatibility flags — the mixin itself doesn't restrict which
  instances can use it. Suitability instead depends on whether
  `self.value` supports ordering at runtime (comparing two incompatible
  types simply falls through to `NotImplemented`).

## Logic
All four operators share the same shape:
1. Unwrap the other operand's `.value` if it's a Simple instance,
   otherwise use it as-is.
2. Compare `self.value` against that.
3. On `TypeError` (values that can't be ordered against each other),
   return `NotImplemented` rather than raising — this lets Python fall
   back to the other operand's comparison method, or raise its own
   standard `TypeError` if neither side can handle it.

## Notes
- `__eq__` is intentionally not defined here — see `Equality` for that;
  combine both when full comparison support is needed.
- Comparing against a raw value doesn't require it to also be a Simple
  instance — `age < 30` works directly.
"""
