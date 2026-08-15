from .InnersProperty import InnersProperty
from .MetaShortcuts import MetaShortcuts


_DESIGN_NOTES = """
# Properties Mixins

## Purpose
Ergonomic property-based access — direct attribute access to a
composite's inners, and shortcut properties over frequently used
metadata fields.

## Components

| Component           | Type  | Description                                                         |
| :------------------ | :---- | :------------------------------------------------------------------ |
| `InnersProperty`    | Mixin | Generates direct-access properties for a composite's inners.        |
| `MetaShortcuts`     | Mixin | Exposes `is_atom`, `is_composite`, `name_snake`, etc. from `meta`.  |

## Notes
- `InnersProperty` is `_composite_only` and uses
  `__extend_instance_class__`; `MetaShortcuts` has no compatibility
  restrictions and adds no new behavior beyond passthrough properties.
"""
