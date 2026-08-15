from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.representation import ValueDisplayProtocol


class ValueFormatting(SimpleMixin):
    """
    Representation and conversion dunders tied to the object's value.
    Does not touch __repr__ / __str__ — those are defined in
    InstanceBase.
    Works for both atomic and composite types, since both have a value.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods = FORMAT
    # ----------------------------------------

    def format(
        self: "ValueDisplayProtocol",
        pattern: str | None = None
    ) -> str:
        """
        Formats the instance's value according to the given pattern.
        If no pattern is given, uses the mask from metadata (meta.mask),
        if it exists. Suitable for formatting numbers, text, and simple
        composite values.
        """
        value = self.value
        mask = pattern or getattr(self.meta, "mask", None)

        if mask and isinstance(value, (str, int, float)):
            return mask.format(value)

        return str(value)

    def __format__(
        self,
        format_spec: str = ""
    ) -> str:
        """
        Support for f-string formatting.
        Enables syntax like: f"{obj:pattern}".
        """
        return self.format(format_spec or None)

    # ----------------------------------------
    # Methods = BYTES / BOOL
    # ----------------------------------------

    def __bytes__(
        self: "ValueDisplayProtocol"
    ) -> bytes:
        """
        Converts the instance's value to bytes.
        Supports:
            - bytes -> returned directly
            - bytearray, memoryview -> bytes(...)
            - str -> UTF-8 encode
        Other types raise TypeError.
        """
        value = self.value

        if isinstance(value, bytes):
            return value

        if isinstance(value, (bytearray, memoryview)):
            return bytes(value)

        if isinstance(value, str):
            return value.encode("utf-8")

        raise TypeError(
            f"Cannot convert {self.meta.class_name} "
            f"(type={type(value).__name__}) to bytes."
        )

    def __bool__(
        self: "ValueDisplayProtocol"
    ) -> bool:
        """
        The object's truthiness matches the truthiness of its value.
        """
        return bool(self.value)


_DESIGN_NOTES = """
# ValueFormatting

## Purpose
Adds value-driven formatting and conversion behavior — `format()`,
f-string support via `__format__`, `bytes(obj)`, and `bool(obj)` — all
routed through the instance's `.value`, without touching how the object
prints via `__repr__`/`__str__` (that's `ValueDisplay`'s job, or the
default from `InstanceBase`).

## Compatibility
- No compatibility flags — unlike `ValueDisplay`, this mixin is *not*
  constant-only. Both atoms and composites have a `.value`, so both can
  reasonably be formatted, converted to bytes, or tested for truthiness.

## Logic
- `format(pattern)` — uses the given pattern if provided, otherwise falls
  back to `meta.mask` if the blueprint declared one. The mask is only
  applied to `str`/`int`/`float` values; anything else just falls back to
  `str(value)`.
- `__format__` is a thin adapter so f-strings work: `f"{obj:pattern}"`
  calls `__format__(pattern)`, which forwards to `format()`.
- `__bytes__` handles the common convertible types explicitly
  (`bytes` passthrough, `bytearray`/`memoryview` via `bytes(...)`, `str`
  via UTF-8 encoding) and raises a descriptive `TypeError` for anything
  else, rather than letting Python's generic bytes-conversion error
  surface.
- `__bool__` simply forwards to `bool(self.value)`, so an instance
  wrapping `0`, `""`, or an empty collection is falsy exactly like the
  raw value would be.

## Notes
- Deliberately independent from `ValueDisplay` — a class can use one,
  both, or neither depending on whether it needs value-like *printing*,
  value-like *formatting/conversion*, or both.
- `meta.mask` is an optional, blueprint-level setting; its absence is not
  an error, `format()` just degrades to `str(value)`.
"""
