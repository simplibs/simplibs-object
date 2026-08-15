from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Inners
from .PickleStateProtocol import PickleStateProtocol
# Annotations
if TYPE_CHECKING:
    from .internal_types import PicklePlan


@runtime_checkable
class PickleReduceProtocol(
    PickleStateProtocol,
    Protocol
):
    """
    Protocol for the PickleReduce mixin.

    Guarantees integration with the low-level pickle protocol via the
    __reduce__ method, defining the factory reconstruction plan for the object.
    """

    def __reduce__(self) -> "PicklePlan":
        """
        Native Python pickle protocol.

        Returns a triplet containing:
        1. Class object for instance recreation (self.__class__)
        2. Empty tuple of positional constructor arguments
        3. State dictionary retrieved via __getstate__()
        """
        ...