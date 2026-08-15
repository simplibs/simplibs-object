from .PicklePlan import PicklePlan

_DESIGN_NOTES = """
# Lifecycles Internal Types Sub-Package

## Purpose
Provides type definitions for object lifecycle operations, specifically pickle reconstruction tuples.

## Internal Components Registry

| Component    | Type      | Description                                                                  |
| :----------- | :-------- | :--------------------------------------------------------------------------- |
| `PicklePlan` | TypeAlias | Tuple structure defining class, empty arguments, and state dictionary for pickle.|
"""