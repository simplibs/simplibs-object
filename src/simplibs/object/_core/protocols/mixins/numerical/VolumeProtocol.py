from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Outers
from ..base_class import SimpleMixinProtocol
# Annotations
if TYPE_CHECKING:
    from .stepper import StepperProtocol


@runtime_checkable
class VolumeProtocol(
    SimpleMixinProtocol,
    Protocol
):
    """
    Protocol for the Volume mixin.

    Guarantees the presence of a numerical controller (stepper) bound directly
    to the main value of the instance, enabling safe stepping and limit enforcement.
    """

    # --- TECHNICAL ATTRIBUTES (Initialized in init_mixins) ---
    _value_stepper: "StepperProtocol"

    # --- PUBLIC API / PROPERTIES ---

    @property
    def value_stepper(self) -> "StepperProtocol":
        """
        Returns the numerical controller (stepper) for safe manipulation
        of the main value of this instance.
        """
        ...