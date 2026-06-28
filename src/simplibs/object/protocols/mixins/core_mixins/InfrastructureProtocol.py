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
    Protokol pro společné infrastrukturní zázemí (uzly a snapshoty) vyžadované
    pro logiky neměnnosti, serializace a reaktivního volání.
    """
