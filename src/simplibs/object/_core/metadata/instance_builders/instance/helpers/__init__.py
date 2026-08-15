from .create_instance_class import create_instance_class
from .get_base_class import get_base_class


_DESIGN_NOTES = """
# Instance Helper Sub-Package

## Purpose
Provides core helper functions used during instance class construction. Handles
structural base-class resolution and dynamic class synthesis for runtime
instances.

## Internal Components Registry

| Component               | Type     | Description                                                |
| :---------------------- | :------- | :--------------------------------------------------------- |
| `create_instance_class` | Function | Builds the unified runtime class from mixins and base class. |
| `get_base_class`        | Function | Resolves the correct structural base class (atom/composite). |
"""
