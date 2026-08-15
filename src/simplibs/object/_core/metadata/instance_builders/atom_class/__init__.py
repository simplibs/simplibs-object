from .InstanceBase import InstanceBase
from .make_atom_class import make_atom_class

_DESIGN_NOTES = """
# Atomic Class Builder Sub-Package

## Purpose
Orchestrates the dynamic type generation and baseline execution blueprints for atomic leaf object representations.

## Internal Components Registry

| Component         | Type     | Description                                                                          |
| :---------------- | :------- | :----------------------------------------------------------------------------------- |
| `InstanceBase`    | Class    | Provides the foundational abstract inheritance layer for compiled object instances.  |
| `make_atom_class` | Function | The primary orchestrator factory function compiling functional atomic runtime types. |
"""