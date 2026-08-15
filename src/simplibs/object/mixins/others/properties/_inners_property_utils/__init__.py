from .collect_all_nested_properties import collect_all_nested_properties


_DESIGN_NOTES = """
# Inners Property Utilities

## Purpose
Provides helper utilities used by the property subsystem to generate nested
properties for composite Simple objects. These utilities traverse metadata
structures and create fully qualified Python properties for deeply nested
inner elements.

## Components

| Component                       | Type     | Description                                                         |
| :------------------------------ | :--------| :------------------------------------------------------------------ |
| `collect_all_nested_properties` | Function | Entry point that collects properties for all nested inner elements. |

## Notes
- This package is internal and not part of the public API.
- Recursive traversal is delegated to `_collect_nested_inner_properties`.
- The design emphasizes clarity, modularity, and deterministic behavior.
"""
