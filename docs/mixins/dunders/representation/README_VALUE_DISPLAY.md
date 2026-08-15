from typing import TYPE_CHECKING
# Outers
from ...base_class import SimpleMixin
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.dunders.representation import ValueDisplayProtocol


class ValueDisplay(SimpleMixin):
    """
    Overrides __repr__ and __str__ so the object presents itself as the
    raw value it wraps.

    Changes how the object is displayed so it represents its value.
    Intended only for atomic (constant-only) types that should behave as
    "value-like" objects (e.g. Decimal, UUID, PhoneNumber...).

    ValueDisplay is a common mixin, but it is not a standard one — it is
    a specialized, opt-in, constant-only mixin, meant to be used only
    when you want the object to behave like a "value object" (e.g.
    Decimal, UUID, Path, Enum, ...).
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _constant_only = True

    # Slot definition
    __slots__ = ()

    # ----------------------------------------
    # Methods - REPR / STR
    # ----------------------------------------

    def __repr__(
        self: "ValueDisplayProtocol"
    ) -> str:
        """
        Technical representation of the object in the format:
            ClassName(value_repr)
        Used for debugging and logging.
        """
        return f"{self.meta.class_name}({self.value!r})"

    def __str__(
        self: "ValueDisplayProtocol"
    ) -> str:
        """
        User-facing representation of the object.
        Returns the plain value converted to a string.
        """
        return str(self.value)


_DESIGN_NOTES = """
# ValueDisplay

## Purpose
Makes an atomic instance *look and print* like the raw value it wraps,
instead of like a generic object. With this mixin, `print(price)` shows
`19.99`, not something like `<SimpleConstant object at 0x...>`.

> For newcomers: `__repr__` is the "developer-facing" representation
> (what you see in a debugger, a REPL, or inside a list/dict print),
> while `__str__` is the "user-facing" one (what `print()` and `str()`
> use). This mixin gives each a distinct but related shape.

## Compatibility
- `_constant_only = True` — this is a deliberate opt-in restriction, not
  a technical limitation. Value-like display only makes sense for atoms
  that model a single "value" (`Decimal`, `UUID`, `PhoneNumber`,
  `Path`-like types) — not for composites, which are made of multiple
  named parts and are better served by a structural, field-by-field
  representation (see `InstanceBase`'s default `__repr__`/`__str__`,
  which this mixin deliberately does *not* touch on composites).

## Logic
- `__repr__` returns `ClassName(value_repr)` — keeps the class identity
  visible (so `PhoneNumber('+420...')` still tells you what it is) while
  showing the wrapped value using its own `repr()`.
- `__str__` returns just `str(self.value)` — drops the class name
  entirely, so the object reads exactly like its underlying value in
  print statements, f-strings, and string concatenation.

## Notes
- Opt-in by design: most Simple instances should *not* use this mixin,
  since hiding the class identity from `str()` can be misleading for
  types where "which class this is" matters more than "what the raw
  value looks like."
- Pairs naturally with `ValueFormatting`, which adds `format()`/
  `__format__`/`__bytes__`/`__bool__` without touching `__repr__`/
  `__str__` — the two mixins split representation concerns cleanly.
"""
