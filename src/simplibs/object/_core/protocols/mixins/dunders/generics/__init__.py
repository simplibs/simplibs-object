from .ClassGetItemProtocol import ClassGetItemProtocol

_DESIGN_NOTES = """
# Generics Dunder Protocols Sub-Package

## Purpose
Provides protocols enabling class-level indexing and generic type hints support without runtime performance penalties.

## Internal Components Registry

| Component              | Type     | Description                                                                  |
| :--------------------- | :------- | :--------------------------------------------------------------------------- |
| `ClassGetItemProtocol` | Protocol | Interface guaranteeing class-level generic subscripting via `__class_getitem__`.|
"""