from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..core_mixins import NodesTupleProtocol
# Annotations
if TYPE_CHECKING:
    from .stepper import StepperProtocol
    from .internal_types import SteppersMap


@runtime_checkable
class EqualizerProtocol(
    NodesTupleProtocol,
    Protocol
):
    """
    Protocol for the Equalizer mixin.

    Guarantees the presence of numerical controllers (steppers) for all sub-node elements
    of a composition. These controllers are generated dynamically based on a blueprint
    and are accessible via dynamic properties with a designated suffix.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---

    # Maps internal element name_snake keys directly to their respective instance Steppers
    _steppers: "SteppersMap"

    # --- DYNAMIC PROPERTY ACCESS ---

    def __getattr__(self, name: str) -> "StepperProtocol":
        """
        Dynamic fallback for accessing generated stepper properties of individual nodes
        (e.g., accessing `obj.node_stepper`).

        Guarantees that every dynamically returned controller strictly conforms to StepperProtocol.
        """
        ...