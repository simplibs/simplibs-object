from typing import Protocol, runtime_checkable
# Inners
from .CopyableProtocol import CopyableProtocol
from .PickleReduceProtocol import PickleReduceProtocol


@runtime_checkable
class LifecycleProtocol(
    CopyableProtocol,
    PickleReduceProtocol,
    Protocol
):
    """
    Protocol for the master Lifecycle mixin.

    Encompasses the complete Python lifecycle of an instance. Fully combines
    safe replication capabilities (shallow and deep copying) with low-level
    support for state persistence, restoration, and reduction (pickle protocol).
    """

    # The master mixin itself acts solely as a structural aggregator, declaring no additional slots or methods.
