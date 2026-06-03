"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class FloatMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __float__(self):
        try:
            return float(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"Nelze převést {self.__class__.__name__} na int: {e}")



__DOCT__ = """
**Purpose:**
Defines conversion to `float`. Called by `float(obj)`. Also called by many math functions
when they expect a real number. Must return a Python `float` (not a subclass).

**Signature:**
```python
def __float__(self) -> float:
    return float(self.value)
```

**Called automatically when:**
```python
float(obj)
```

**Relationships:** Paired with `__int__`, `__complex__`. `__float__` is also a fallback when `__complex__` is missing.
"""