"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance
import math


class CeilMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __ceil__(self):
        try:
            return math.ceil(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"Nelze převést {self.__class__.__name__} na int: {e}")



__DOCT__ = """
**Purpose:**
Implements `math.ceil(obj)` — rounds *up* to the nearest integer (toward +∞).
Must return an `int`.

**Signature:**
```python
def __ceil__(self) -> int:
    import math
    return math.ceil(self.value)
```

**Called automatically when:**
```python
import math
math.ceil(obj)   # calls obj.__ceil__()
```

**Relationships:** Sibling of `__floor__` and `__round__`. Contrast: `__floor__` rounds toward -∞.
"""