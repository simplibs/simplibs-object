from .ArithmeticProtocol import ArithmeticProtocol
from .BitwiseProtocol import BitwiseProtocol
from .ConversionProtocol import ConversionProtocol
from .InplaceProtocol import InplaceProtocol
from .UnaryProtocol import UnaryProtocol

_DESIGN_NOTES = """
# Numeric Dunder Protocols Sub-Package

## Purpose
Defines mathematical, bitwise, unary, and in-place operator protocols for underlying object values.

## Internal Components Registry

| Component            | Type     | Description                                                                  |
| :------------------- | :------- | :--------------------------------------------------------------------------- |
| `ArithmeticProtocol` | Protocol | Standard and right-hand arithmetic operators (`+`, `-`, `*`, `/`, etc.).     |
| `BitwiseProtocol`    | Protocol | Bitwise logical operators (`&`, `|`, `^`, `<<`, `>>`, `~`).                 |
| `ConversionProtocol` | Protocol | Native type conversion (`int`, `float`, `complex`) and rounding math functions.|
| `InplaceProtocol`    | Protocol | In-place arithmetic assignment operators (`+=`, `-=`, `*=`, etc.).           |
| `UnaryProtocol`      | Protocol | Unary mathematical sign and absolute value operators (`-x`, `+x`, `abs(x)`). |
"""