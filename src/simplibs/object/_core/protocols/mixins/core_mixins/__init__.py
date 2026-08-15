from .NodesDictsProtocol import NodesDictsProtocol
from .NodesTupleProtocol import NodesTupleProtocol
from .SnapshotProtocol import SnapshotProtocol
from .SerializationProtocol import SerializationProtocol
from .InfrastructureProtocol import InfrastructureProtocol

from typing import TypeVar
InfrastructuredComponent = TypeVar("InfrastructuredComponent", bound="InfrastructureProtocol")


_DESIGN_NOTES = """
# Core Mixin Protocols Sub-Package

## Purpose
Provides foundational protocols for internal object graph navigation, fast lookup mappings,
state snapshotting, core infrastructure, and full serialization support.

## Internal Components Registry

| Component                | Type     | Description                                                                  |
| :----------------------- | :------- | :--------------------------------------------------------------------------- |
| `NodesTupleProtocol`     | Protocol | Primary source of truth for sub-node flattened tuple structures.             |
| `NodesDictsProtocol`     | Protocol | Immutable O(1) lookup dictionary mappings by sub-node semantic names.       |
| `SnapshotProtocol`       | Protocol | Interface for state creation, restoration, and diff comparison.              |
| `InfrastructureProtocol` | Protocol | Shared infrastructure backbone uniting node graphs and snapshots.            |
| `SerializationProtocol`  | Protocol | Master import/export interface supporting JSON, dicts, and fluent updates.   |
"""