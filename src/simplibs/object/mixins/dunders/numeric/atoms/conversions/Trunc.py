"""
Konverze jako __ceil__, __floor__, __round__, __int__, __float__, __complex__
— ty by správně neměly vracet NotImplemented při chybě, ale vyhazovat TypeError.
Python runtime totiž NotImplemented z těchto metod neakceptuje a chová se nepředvídatelně.
Zatím to nech jak je, ale tohle bude chtít opravu v dalším kole.

"""


# numeric/conversions/Trunc.py
class TruncMixin:
    __slots__ = ()
    value: Any

    def __trunc__(self):
        try:
            import math
            return math.trunc(self.value)
        except (TypeError, ValueError):
            # runtime neakceptuje NotImplemented z conversion metod.
            # Musí buď vrátit hodnotu, nebo vyhodit TypeError.
            raise TypeError(f"math.trunc() nelze aplikovat na {self.__class__.__name__}")

__DOCT__ = """
**Purpose:**
`__trunc__` is called by `math.trunc(obj)` and is also the *fallback* that `int()` uses
when `__int__` is not defined (as of Python 3.11, this fallback emits a
`DeprecationWarning`; in future versions it will be removed). It should return the integer
closest to zero (i.e., truncate toward zero, not toward -∞ like `__floor__`).
`math.trunc(2.9)` → 2, `math.trunc(-2.9)` → -2.

**Signature:**
```python
def __trunc__(self) -> int:
    import math
    return math.trunc(self._value)
```

**Called automatically when:**
```python
import math
math.trunc(obj)    # calls obj.__trunc__()
int(obj)           # fallback if __int__ is not defined (deprecated path)
```

**Relationships:**
- Part of the rounding family: `__trunc__` (toward zero), `__floor__` (toward -∞), `__ceil__` (toward +∞).
- Belongs conceptually next to `numeric/conversions/Floor.py` and `numeric/conversions/Ceil.py`.
- Prefer defining `__int__` + `__index__` over relying on `__trunc__` as an `int()` fallback.
"""