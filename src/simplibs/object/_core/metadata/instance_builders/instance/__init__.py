from .create_instance import create_instance


_DESIGN_NOTES = """
# Instance Builder Sub-Package

## Purpose
Provides the primary high-level orchestrator responsible for constructing runtime instances.
Coordinates validation, structural topology resolution, dynamic class synthesis,
mixin extensions, raw memory allocation, and initialization.

## Internal Components Registry

| Component         | Type     | Description                                         |
| :---------------- | :------- | :-------------------------------------------------- |
| `create_instance` | Function | Orchestrates the complete instance lifecycle pipeline. |
"""