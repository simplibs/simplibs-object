from .create_instance import create_instance


_DESIGN_NOTES = """
# Instance Builder Sub-Package

## Purpose
Provides the main factory function responsible for constructing runtime
instances. Coordinates validation, structural resolution, class synthesis,
mixin extensions, memory allocation, and initialization.

## Internal Components Registry

| Component         | Type     | Description                                      |
| :---------------- | :------- | :----------------------------------------------- |
| `create_instance` | Function | Orchestrates the full instance creation pipeline. |
"""
