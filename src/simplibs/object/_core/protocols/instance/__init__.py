from .core_classes import InstanceBaseProtocol, AtomInstanceProtocol, CompositeInstanceProtocol
from .SimpleInstanceBaseProtocol import SimpleInstanceBaseProtocol
from .SimpleConstantInstanceProtocol import SimpleConstantInstanceProtocol
from .SimpleObjectInstanceProtocol import SimpleObjectInstanceProtocol

# Element defining the largest set (superset for annotations)
SimpleInstanceClassLike = CompositeInstanceProtocol
SimpleInstanceLike = SimpleObjectInstanceProtocol

# Element defining the smallest set (minimal interface for type verification)
SimpleInstanceClassType = AtomInstanceProtocol
SimpleInstanceType = SimpleConstantInstanceProtocol


_DESIGN_NOTES = """
# Instance Protocols Sub-Package

## Purpose
Exposes public runtime instance protocols that combine core class behaviors with factory-injected
technical attributes (mutability, constant indicators, and mixin tuples).

## Internal Components Registry

| Component                        | Type     | Description                                                              |
| :------------------------------- | :------- | :----------------------------------------------------------------------- |
| `SimpleInstanceBaseProtocol`     | Protocol | Root protocol encompassing technical attributes from factory instantiation|
| `SimpleConstantInstanceProtocol` | Protocol | Complete protocol interface for final constant/atomic runtime instances. |
| `SimpleObjectInstanceProtocol`   | Protocol | Complete protocol interface for final composite runtime instances.       |
"""