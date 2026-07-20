from .calculate_blueprint_path import calculate_blueprint_path


_DESIGN_NOTES = """
# Class Blueprint Path Sub-Package

## Purpose
Provides structural utilities for analyzing class inheritance hierarchies and deriving human-readable lineage indicators used in diagnostic reporting and technical representations.

## Internal Components Registry

| Component                  | Type     | Description                                                                          |
| :------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `calculate_blueprint_path` | Function | Traverses the MRO to build a deterministic representation of a class's custom parents. |
"""