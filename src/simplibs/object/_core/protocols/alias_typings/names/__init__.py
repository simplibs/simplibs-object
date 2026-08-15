from .NamesSet import NamesSet
from .NamesTuple import NamesTuple

_DESIGN_NOTES = """
# Names Alias Typings Sub-Package

## Purpose
Provides collection type definitions for element names as unordered sets or ordered tuples.

## Internal Components Registry

| Component    | Type      | Description                                                                  |
| :----------- | :-------- | :--------------------------------------------------------------------------- |
| `NamesSet`   | TypeAlias | Unordered set container storing unique registered element names.            |
| `NamesTuple` | TypeAlias | Immutable ordered tuple holding registered element name strings.              |
"""