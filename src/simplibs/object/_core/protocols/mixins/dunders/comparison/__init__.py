from .EqualityProtocol import EqualityProtocol
from .OrderingProtocol import OrderingProtocol

_DESIGN_NOTES = """
# Comparison Dunder Protocols Sub-Package

## Purpose
Defines protocols for object equality checks, hashing, and ordering comparisons across the object hierarchy.

## Internal Components Registry

| Component          | Type     | Description                                                                  |
| :----------------- | :------- | :--------------------------------------------------------------------------- |
| `EqualityProtocol` | Protocol | Interface for equality (`__eq__`, `__ne__`) and hashing (`__hash__`).        |
| `OrderingProtocol` | Protocol | Interface for rich comparison operators (`<`, `<=`, `>`, `>=`).               |
"""