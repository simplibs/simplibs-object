from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class LshiftMixin(ModifyInstance):
    __slots__ = ()

    value: Any


    def __lshift__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value << other_value)
        except TypeError:
            return NotImplemented

    def __rlshift__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value << self.value)
        except TypeError:
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements `<<` left bit-shift. Shifts bits left by n positions, equivalent to
multiplying by 2ⁿ (without overflow in Python's arbitrary-precision integers).

**Signature:**
```python
def __lshift__(self, n):
    return type(self)(self.value << n)

def __rlshift__(self, other): ...
def __ilshift__(self, n): self.value <<= n; return self
```

**Called automatically when:** `a << n`
"""