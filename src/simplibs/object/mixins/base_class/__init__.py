from .SimpleMixin import SimpleMixin

_DESIGN_NOTES = """
# Simple Mixin Base Package

## Purpose
Provides the foundational interface for all mixins in the Simple system.
This package defines the `SimpleMixin` class, which establishes the structural
contract, declarative compatibility flags, initialization hook, and automatic
validation pipeline for mixin subclasses.

## Internal Components Registry

| Component     | Type   | Description                                                             |
| :------------ | :----- | :---------------------------------------------------------------------- |
| `SimpleMixin` | Class  | Base class for all mixins; enforces structural rules via subclass init. |
"""
