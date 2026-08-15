from typing import Protocol, runtime_checkable, Any, Self
# Outers
from ...core_mixins import InfrastructureProtocol


@runtime_checkable
class CallProtocol(
    InfrastructureProtocol,
    Protocol
):
    """
    Protocol for the Call mixin.

    Guarantees the ability to call an instance like a function (obj(...)) for
    bulk updates and internal state transformations. Returns a modified version
    of the same type (Self).
    """

    def __call__(self, *changes: Any, **kwargs: Any) -> Self:
        """
        Allows calling the instance as a function and applying changes to it.

        Supports both positional arguments (tuples, variations of tuples) and
        keyword arguments (kwargs). Delegates all execution logic to the with_any engine.
        """
        ...