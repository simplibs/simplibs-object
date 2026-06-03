from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class XorMixin(ModifyInstance):
    __slots__ = ()

    value: Any


    def __xor__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value ^ other_value)
        except TypeError:
            return NotImplemented

    def __rxor__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value ^ self.value)
        except TypeError:
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements `^` bitwise XOR (exclusive OR). A bit is 1 if the operands differ in
that position. Also used for set symmetric difference.

**Signature:**
```python
def __xor__(self, other):
    return type(self)(self.value ^ other.value)

def __rxor__(self, other): ...
def __ixor__(self, other): self.value ^= other.value; return self
```

**Called automatically when:**
```python
a ^ b    # __xor__
a ^= b   # __ixor__
```

**Relationships:** Reflected: `__rxor__` · In-place: `__ixor__`
"""