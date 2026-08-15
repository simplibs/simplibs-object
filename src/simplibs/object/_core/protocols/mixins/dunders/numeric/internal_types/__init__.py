from .Operator import Operator
from .UnaryOperator import UnaryOperator

_DESIGN_NOTES = """
# Numeric Internal Types Sub-Package

## Purpose
Provides type aliases for standard binary and unary operator callables from Python's operator module.

## Internal Components Registry

| Component       | Type      | Description                                                                  |
| :-------------- | :-------- | :--------------------------------------------------------------------------- |
| `Operator`      | TypeAlias | Binary operator function accepting two arguments and returning a result.    |
| `UnaryOperator` | TypeAlias | Unary operator function accepting a single argument and returning a result.  |
"""