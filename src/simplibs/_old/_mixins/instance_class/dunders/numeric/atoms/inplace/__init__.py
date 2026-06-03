from .Iadd import IaddMixin
from .Idiv import IdivMixin
from .Ifloordiv import IfloordivMixin
from .Imod import ImodMixin
from .Imul import ImulMixin
from .Ipow import IpowMixin
from .Isub import IsubMixin

__all__ = (
    "IaddMixin",
    "IdivMixin",
    "IfloordivMixin",
    "ImodMixin",
    "ImulMixin",
    "IpowMixin",
    "IsubMixin",
)


__DOCT__ = """
## `numeric/inplace/`

> **Subgroup purpose:**
> In-place ("augmented assignment") operators like `+=`, `-=`, `*=`, etc.
> If an in-place dunder is not defined, Python falls back to the regular binary operator
> and reassigns — so `a += b` becomes `a = a + b`. Define the in-place version when
> mutation is cheaper than creating a new object (e.g., appending to a list in-place
> vs. creating a new list).
"""