from .calculate_value import calculate_value
from .decompose_value import decompose_value

_DESIGN_NOTES = """
# Object Methods Sub-Package

## Purpose
Provides the core functional building blocks used by `SimpleObject` classes to
perform composite value calculation, decomposition, and structured parameter
processing.

## Internal Components Registry

| Component                          | Type     | Description                                                                |
| :--------------------------------- | :------- | :------------------------------------------------------------------------- |
| `calculate_value`                  | Function | Computes composite values using the user-defined `_logic` method.          |
| `decompose_value`                  | Function | Decomposes composite values using the user-defined `_decompose` method.    |
"""
