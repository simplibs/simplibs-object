from typing import TYPE_CHECKING
from numbers import Number
# Outers
from ..base_class import SimpleMixin
# Innser
from ._stepper_class import Stepper
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.numerical import VolumeProtocol
    from ...._core.protocols.mixins.numerical.stepper import StepperProtocol


class Volume(SimpleMixin):
    """
    Provides access to a stepper for the main value.

    Guarantees the presence of a numeric controller (stepper) attached
    directly to the instance's main value, enabling safe stepping and
    limit enforcement.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _mutable_only = True
    _only_types = Number

    # Slot definition
    __slots__ = ("_value_stepper",)

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "VolumeProtocol"
    ) -> None:
        """
        Method forwarding its logic into the instance's initialization
        process.
        """

        # 1. Initialize parents
        super().init_mixins()

        # 2. Stepper for the base value
        self._value_stepper: "StepperProtocol" = Stepper(self)

    # ----------------------------------------
    # Property - getters
    # ----------------------------------------

    @property
    def value_stepper(
        self: "VolumeProtocol"
    ) -> "StepperProtocol":
        """
        Returns the numeric controller (stepper) for safely manipulating
        this instance's main value.
        """
        return self._value_stepper


_DESIGN_NOTES = """
# Volume

## Purpose
Attaches a `Stepper` — a numeric controller supporting safe stepping and
limit enforcement — directly to an instance's own value. Named "Volume"
for the mental image of a volume knob: turn it up/down safely, without
overshooting bounds.

> For newcomers: a naive `obj.value += 1` has no built-in concept of
> "don't go above 100" or "clamp at 0." A `Stepper` wraps that logic once,
> so callers can step values up/down without re-implementing bounds
> checking everywhere.

## Compatibility
- `_mutable_only = True` — stepping is an in-place operation on the
  instance's own value; on an immutable instance there'd be nothing to
  step in place.
- `_only_types = Number` — a stepper's increment/decrement/clamp logic
  only makes sense for numeric values.

## Logic
On `init_mixins`, a single `Stepper(self)` is built and stored as
`_value_stepper`, exposed publicly through the read-only `value_stepper`
property. All the actual stepping/clamping logic lives inside the
`Stepper` class itself (`_stepper_class`) — this mixin's only job is to
construct one, bound to `self`, and expose it.

## Notes
- Compare with `Equalizer`, which does the same thing but for every
  *inner* of a composite (one stepper per node) rather than for the
  instance's own single value — `Volume` is the atom/single-value
  counterpart to `Equalizer`'s per-inner version.
- The property is named `value_stepper`, distinct from the private
  `_value_stepper` slot — the usual public/private naming split used
  throughout the ecosystem.
"""
