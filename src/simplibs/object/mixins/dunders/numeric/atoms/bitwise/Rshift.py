from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class RshiftMixin(ModifyInstance):
    __slots__ = ()

    value: Any


    def __rshift__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value >> other_value)
        except TypeError:
            return NotImplemented

    def __rrshift__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value >> self.value)
        except TypeError:
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements `>>` right bit-shift. Shifts bits right by n positions (arithmetic shift —
sign bit is preserved for negative numbers), equivalent to dividing by 2ⁿ.

**Signature:**
```python
def __rshift__(self, n):
    return type(self)(self.value >> n)

def __rrshift__(self, other): ...
def __irshift__(self, n): self.value >>= n; return self
```

**Called automatically when:** `a >> n`
"""