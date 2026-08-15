from typing import Protocol, runtime_checkable
# Inners
from .NodesDictsProtocol import NodesDictsProtocol
from .SnapshotProtocol import SnapshotProtocol


@runtime_checkable
class InfrastructureProtocol(
    NodesDictsProtocol,
    SnapshotProtocol,
    Protocol
):
    """
    Protocol for shared infrastructure components (nodes and snapshots) required
    for immutability logic, serialization, and reactive execution.
    """