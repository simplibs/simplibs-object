from .PathDict import PathDict
from .PathTuple import PathTuple

_DESIGN_NOTES = """
# Paths Alias Typings Sub-Package

## Purpose
Provides type definitions for hierarchical semantic paths and key-to-path registry mappings.

## Internal Components Registry

| Component   | Type      | Description                                                                  |
| :---------- | :-------- | :--------------------------------------------------------------------------- |
| `PathDict`  | TypeAlias | Key-value dictionary mapping element identifiers to their path tuples.       |
| `PathTuple` | TypeAlias | Immutable tuple of string tokens representing a hierarchical path.           |
"""