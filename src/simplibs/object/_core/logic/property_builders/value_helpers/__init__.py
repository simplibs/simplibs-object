from .create_value_getter import create_value_getter
from .create_value_setter import create_value_setter

_DESIGN_NOTES = """
# Property Value Helpers Sub-Package

## Purpose
Contains low-level functional generators used internally by property builders.
These helpers encapsulate the core logic for reading and mutating normalized
values stored inside atomic and composite instances.

## Internal Components Registry

| Component             | Type     | Description                                                                |
| :-------------------- | :------- | :------------------------------------------------------------------------- |
| `create_value_getter` | Function | Generates optimized getter closures for root and inner value access.       |
| `create_value_setter` | Function | Generates setter closures handling normalization, decomposition, and logs. |
"""
