from .NodesDictsProtocol import NodesDictsProtocol
from .NodesTupleProtocol import NodesTupleProtocol
from .SnapshotProtocol import SnapshotProtocol
from .SerializationProtocol import SerializationProtocol
from .InfrastructureProtocol import InfrastructureProtocol

from typing import TypeVar
InfrastructuredComponent = TypeVar("InfrastructuredComponent", bound="InfrastructureProtocol")