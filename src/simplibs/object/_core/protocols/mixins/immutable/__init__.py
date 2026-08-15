from .ImmutableMethodsProtocol import ImmutableMethodsProtocol
from .ImmutableMethodsWithInnersProtocol import ImmutableMethodsWithInnersProtocol


_DESIGN_NOTES = """
# Immutable Mixin Protocols Sub-Package

## Purpose
Defines protocols for functional, immutable state transformations that produce new updated
instances without mutating existing objects.

## Internal Components Registry

| Component                             | Type     | Description                                                                  |
| :------------------------------------ | :------- | :--------------------------------------------------------------------------- |
| `ImmutableMethodsProtocol`           | Protocol | Core functional interface for immutable constants, composites, and copies.  |
| `ImmutableMethodsWithInnersProtocol`  | Protocol | Dynamic attribute fallback (`__getattr__`) for generated inner node setters.  |
"""