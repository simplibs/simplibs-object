from .SimpleBaseProtocol import SimpleBaseProtocol
from .SimpleConstantProtocol import SimpleConstantProtocol
from .SimpleObjectProtocol import SimpleObjectProtocol

# Element defining the largest set (superset for annotations)
SimpleClassLike = SimpleObjectProtocol

# Element defining the smallest set (minimal interface for type verification)
SimpleClassType = SimpleBaseProtocol


_DESIGN_NOTES = """
# Classes Protocols Sub-Package

## Purpose
Defines structural protocols for definition template classes (`SimpleBase`, `SimpleConstant`, `SimpleObject`),
establishing the contract for class-level validation, computational logic, and metadata access.

## Internal Components Registry

| Component                | Type     | Description                                                                 |
| :----------------------- | :------- | :-------------------------------------------------------------------------- |
| `SimpleBaseProtocol`     | Protocol | Base interface shared across all definition classes with metadata access.   |
| `SimpleConstantProtocol` | Protocol | Contract for atomic constant classes with validation and normalization.     |
| `SimpleObjectProtocol`   | Protocol | Contract for composite object classes with `_logic` signature propagation.  |
"""