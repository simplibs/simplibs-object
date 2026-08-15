from .CallProtocol import CallProtocol
from .ContextProtocol import ContextProtocol

_DESIGN_NOTES = """
# Interfaces Dunder Protocols Sub-Package

## Purpose
Defines protocols for callable instances and context management scoping within Python execution blocks.

## Internal Components Registry

| Component         | Type     | Description                                                                  |
| :---------------- | :------- | :--------------------------------------------------------------------------- |
| `CallProtocol`    | Protocol | Interface enabling instance invocation as a function for state updates.      |
| `ContextProtocol` | Protocol | Interface for context manager protocol (`__enter__` and `__exit__`).         |
"""