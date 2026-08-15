from .ValueDisplayProtocol import ValueDisplayProtocol
from .ValueFormattingProtocol import ValueFormattingProtocol

_DESIGN_NOTES = """
# Representation Dunder Protocols Sub-Package

## Purpose
Provides protocols for string representation, developer debugging outputs, f-string formatting, and truthiness evaluation.

## Internal Components Registry

| Component                  | Type     | Description                                                                  |
| :------------------------- | :------- | :--------------------------------------------------------------------------- |
| `ValueDisplayProtocol`     | Protocol | Interface for string conversion (`__str__`) and developer repr (`__repr__`).  |
| `ValueFormattingProtocol`  | Protocol | Interface for f-string formatting, byte conversion, and boolean evaluation.  |
"""