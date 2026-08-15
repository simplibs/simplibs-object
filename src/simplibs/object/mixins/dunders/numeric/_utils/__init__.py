from .execute_arithmetic_op import execute_arithmetic_op
from .execute_bitwise_op import execute_bitwise_op
from .execute_conversion import execute_conversion
from .execute_inplace_op import execute_inplace_op
from .execute_unary_op import execute_unary_op


_DESIGN_NOTES = """
# Numeric Dunder Utilities

## Purpose
Provides the internal helper functions used by all numeric dunder mixins.
These utilities implement the core mechanics of:

- safe operand type alignment,
- arithmetic operations (standard & reversed),
- bitwise operations,
- unary operations,
- in-place arithmetic operations,
- native numeric conversions.

They form the computational backbone of the numeric subsystem and ensure
consistent behavior across Arithmetic, Bitwise, Conversion, Inplace, and Unary
mixins.

## Components

| Component                 | Type     | Description                                                        |
| :------------------------ | :--------| :----------------------------------------------------------------- |
| `execute_arithmetic_op`   | Function | Executes arithmetic operations with fallback type alignment.        |
| `execute_bitwise_op`      | Function | Executes bitwise operations with strict operand handling.           |
| `execute_conversion`      | Function | Executes native numeric conversions with unified error formatting.  |
| `execute_inplace_op`      | Function | Executes in-place arithmetic operations with safe mutation.         |
| `execute_unary_op`        | Function | Executes unary operations with fallback type alignment.             |

## Notes
- These utilities are internal and not part of the public API.
- They are used exclusively by numeric dunder mixins.
- All structural logic is delegated to the mixins; utilities remain minimal.
- Errors follow unified diagnostic formatting for consistent developer experience.
"""
