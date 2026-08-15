from .InnersMap import InnersMap
from .InnersTuple import InnersTuple

_DESIGN_NOTES = """
# Inners Alias Typings Sub-Package

## Purpose
Provides type definitions for managing inner composition components, lookups, and sequence mappings.

## Internal Components Registry

| Component     | Type      | Description                                                                  |
| :------------ | :-------- | :--------------------------------------------------------------------------- |
| `InnersMap`   | TypeAlias | Dictionary mapping snake_case component names to inner definition classes.   |
| `InnersTuple` | TypeAlias | Tuple holding declared inner component classes for composite architecture.   |
"""