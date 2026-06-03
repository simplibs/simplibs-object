from .And import AndMixin
from .Invert import InvertMixin
from .Lshift import LshiftMixin
from .Or import OrMixin
from .Rshift import RshiftMixin
from .Xor import XorMixin

__all__ = (
    "AndMixin",
    "InvertMixin",
    "LshiftMixin",
    "OrMixin",
    "RshiftMixin",
    "XorMixin",
)


__DOCT__ = """
## `numeric/bitwise/`

> **Subgroup purpose:**
> Bitwise operators work on the binary representation of integers. They are also
> heavily used in Python as *set-like* operations (e.g., `|` for dict merge in 3.9+,
> `&` / `|` for sets). Each has a reflected and in-place variant following the same
> pattern as arithmetic operators.
"""