"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class RoundMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __round__(self, n=None):
        try:
            return round(self.value, n)
        except TypeError:
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"Nelze převést {self.__class__.__name__} na int: {e}")



__DOCT__ = """
**Purpose:**
Implements `round(obj)` and `round(obj, ndigits)`. Python uses *banker's rounding*
(round half to even) by default. The `ndigits` parameter can be negative (e.g.,
`round(1250, -2)` → 1200).

**Signature:**
```python
def __round__(self, ndigits: int = 0):
    return type(self)(round(self.value, ndigits))
```

**Called automatically when:**
```python
round(obj)           # ndigits defaults to 0
round(obj, 2)        # ndigits=2
```

**Relationships:** Sibling of `__ceil__`, `__floor__`.
"""