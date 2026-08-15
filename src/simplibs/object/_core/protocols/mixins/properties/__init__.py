from .MetaShortcutsProtocol import MetaShortcutsProtocol
from .InnersPropertyProtocol import InnersPropertyProtocol


_DESIGN_NOTES = """
# Property Mixin Protocols Sub-Package

## Purpose
Provides protocols for dynamic inner element property access and ergonomic metadata shortcuts.

## Internal Components Registry

| Component                 | Type     | Description                                                                  |
| :------------------------ | :------- | :--------------------------------------------------------------------------- |
| `InnersPropertyProtocol`  | Protocol | Dynamic access interface for sub-node properties generated from blueprints.  |
| `MetaShortcutsProtocol`   | Protocol | Ergonomic properties for fast querying of object identity and metadata.      |
"""