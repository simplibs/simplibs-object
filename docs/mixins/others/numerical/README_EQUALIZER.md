from typing import TYPE_CHECKING
from numbers import Number
# Outers
from ..._common_logic.constants import STEPPER
from ...core_mixins import NodesTuple
# Inners
from ._stepper_class import Stepper
# Annotations
if TYPE_CHECKING:
    from ...._core.protocols.mixins.numerical import EqualizerProtocol
    from ...._core.protocols.mixins.numerical.internal_types import SteppersMap
    from ...._core.protocols.instance import SimpleInstanceLike


class Equalizer(NodesTuple):
    """
    Provides access to a stepper for every inner.

    Guarantees the presence of numeric controllers (steppers) for every
    sub-node element of the composite. These controllers are generated
    dynamically based on the blueprint and are exposed via dynamic
    properties with a suffix.
    """

    # ----------------------------------------
    # Basic interface
    # ----------------------------------------

    # Compatibility declaration
    _composite_only = True
    _mutable_only = True
    _only_types = Number

    # Slot definition
    __slots__ = ("_steppers",)

    # ----------------------------------------
    # Hook for modifying the instance class
    # ----------------------------------------

    @staticmethod
    def __extend_instance_class__(
        instance_cls: "SimpleInstanceLike"
    ) -> "SimpleInstanceLike":
        """
        Internal method for attaching elements to the class, before the
        initialization process.
        """

        # 1. Build the required properties
        for name in instance_cls.meta.node_names_set:

            # 1.1 Getter definition
            def getter(self: "EqualizerProtocol", _name: str = name):
                return self._steppers[_name]

            # 1.2 Set the getter's name and docstring
            prop_name = f"{name}{STEPPER}"
            getter.__name__ = f"get_{prop_name}"
            getter.__doc__ = (
                f"Returns the Stepper object for node `{name}`.\n"
                f"Generated dynamically based on the object's structure."
            )

            # 1.3 Create the property and store it on the class
            setattr(instance_cls, prop_name, property(getter))

        # 2. Return the modified class
        return instance_cls

    # ----------------------------------------
    # Initialization hook
    # ----------------------------------------

    # noinspection PyAttributeOutsideInit
    def init_mixins(
        self: "EqualizerProtocol"
    ) -> None:
        """
        Method forwarding its logic into the instance's initialization
        process.
        """

        # 1. Initialize parents
        super().init_mixins()

        # 2. Dict of steppers for every element
        self._steppers: "SteppersMap" = {
            instance.meta.name_snake: Stepper(instance)
            for instance, _ in self._nodes_tuple
        }


_DESIGN_NOTES = """
# Equalizer

## Purpose
Gives every inner of a composite its own `Stepper`, exposed as a dynamic
property named `<inner_name><STEPPER suffix>` (e.g. `volume_stepper`) —
so each numeric field can be stepped/clamped independently, the way a
mixing-desk equalizer has one fader per channel.

## Compatibility
- `_composite_only = True` — needs inners to attach per-node steppers to;
  an atom is handled instead by `Volume`.
- `_mutable_only = True` / `_only_types = Number` — same reasoning as
  `Volume`: stepping mutates in place, and only makes sense on numbers.

## Logic
Two separate mechanisms work together:

1. `__extend_instance_class__` (class-creation time) — for every node
   name in `meta.node_names_set`, dynamically defines and attaches a
   read-only `property` named `f"{name}{STEPPER}"`. Each property's
   getter closes over its own `name` via the `_name: str = name` default
   argument trick (same pattern as `ImmutableWithInners`), so every
   generated property correctly reads its own entry rather than all
   sharing the last loop value.
2. `init_mixins` (instance-creation time) — builds the actual
   `_steppers` dict, one `Stepper(instance)` per node in `_nodes_tuple`,
   keyed by `name_snake`. The properties defined in step 1 simply read
   from this dict at access time.

## Notes
- Two-phase design is intentional: the *properties* only need to be
  defined once per class (step 1), but the *stepper objects* need to be
  built fresh per instance (step 2), since each instance has its own
  node values to step.
- Compare with `Volume`, which does the single-value equivalent for an
  atom — `Equalizer` is effectively "one `Volume` per inner," generated
  dynamically rather than declared per field.
"""
