"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class IntMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __int__(self):
        try:
            return int(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"Nelze převést {self.__class__.__name__} na int: {e}")



__DOCT__ = """
**Purpose:**
Defines conversion to `int`. Called by `int(obj)`, and also implicitly by Python in
contexts that require an integer (e.g., sequence indexing, `range()`, `struct.pack`).
Should truncate toward zero (same behaviour as `int()` on floats).

**Signature:**
```python
def __int__(self) -> int:
    return int(self.value)
```

**Called automatically when:**
```python
int(obj)       # explicit conversion
# also implicitly in some C-level operations
```

**Relationships:**
- `__index__` is a stricter version: declares the object IS an integer (for slicing, numpy).
  Note: `__index__` is not a separate atom in your structure but lives conceptually near `__int__`.
- `__float__` and `__complex__` for other numeric conversions.
- `__trunc__` is called by `math.trunc()` and is the fallback for `int()`.
"""