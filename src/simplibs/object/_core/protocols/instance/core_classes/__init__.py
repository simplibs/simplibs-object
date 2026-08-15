from .InstanceBaseProtocol import InstanceBaseProtocol
from .AtomInstanceProtocol import AtomInstanceProtocol
from .CompositeInstanceProtocol import CompositeInstanceProtocol

_DESIGN_NOTES = """
# Instance Core Classes Protocols Sub-Package

## Purpose
Provides foundational protocols for low-level runtime instances (atomic units and composite structures),
guaranteeing value management, owner references, and reactive recalculation anchors.

## Internal Components Registry

| Component                   | Type     | Description                                                                  |
| :-------------------------- | :------- | :--------------------------------------------------------------------------- |
| `InstanceBaseProtocol`      | Protocol | Common identity guarantor and mixin initialization anchor for all instances.|
| `AtomInstanceProtocol`      | Protocol | Core interface for atomic leaf instances with value getting/setting.          |
| `CompositeInstanceProtocol` | Protocol | Core interface for composite instances with inner element dynamic access.     |
"""