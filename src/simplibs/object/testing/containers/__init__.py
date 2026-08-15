from .InnerValue import InnerValue
from .MixinCase import MixinCase
from .ObjectCase import ObjectCase
from .TestMixin import TestMixin

_DESIGN_NOTES = """
# Testing Containers Sub-Package

## Purpose
Provides strongly-typed dataclasses and test mixin structures used to configure bulk assertions and test suites.

## Internal Components Registry

| Component    | Type      | Description                                                               |
| :----------- | :-------- | :------------------------------------------------------------------------ |
| `InnerValue` | Dataclass | Holds target path and expected value specs for nested object testing.     |
| `MixinCase`  | Dataclass | Wraps test cases, parameters, and expected behaviors for mixin assertions.|
| `ObjectCase` | Dataclass | Wraps comprehensive test case configurations for `SimpleObject` suites.   |
| `TestMixin`  | Class     | Abstract base class for constructing mixin testing targets.               |
"""