from typing import Protocol, runtime_checkable, Self, Any
# Outers
from ...core_mixins import NodesDictsProtocol, SnapshotProtocol


@runtime_checkable
class CopyableProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for the Copyable mixin.

    Guarantees support for standard shallow and deep copying of objects
    within the Python ecosystem (integration with the copy module). The strategy
    adapts internally to the mutability state while consistently returning the identical type (Self).
    """

    def __copy__(self) -> Self:
        """
        Creates and returns a shallow copy of this instance.
        Safely responds to the object's mutable/immutable mode.
        """
        ...

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        """
        Creates and returns a deep copy of this instance.
        The `memo` dictionary serves to internally track already visited
        objects to prevent recursion cycles.
        """
        ...