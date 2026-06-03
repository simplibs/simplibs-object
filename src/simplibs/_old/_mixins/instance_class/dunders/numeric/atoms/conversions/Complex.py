"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class ComplexMixin(ModifyInstance):
    __slots__ = ()

    value: Any


    def __complex__(self):
        try:
            return complex(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"Nelze převést {self.__class__.__name__} na int: {e}")


__DOCT__ = """
**Purpose:**
Defines conversion to `complex`. Called by `complex(obj)`. Part of the numeric tower:
`int → float → complex`. If your object supports complex representation, define this.

**Signature:**
```python
def __complex__(self) -> complex:
    return complex(self.value)
```

**Called automatically when:**
```python
complex(obj)
```
"""