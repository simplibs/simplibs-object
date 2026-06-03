from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class AndMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __and__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value & other_value)
        except TypeError:
            return NotImplemented

    def __rand__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value & self.value)
        except TypeError:
            return NotImplemented




__DOCT__ = """
**Purpose:**
Implements the `&` bitwise AND operator. Each bit in the result is 1 only if the
corresponding bits in both operands are 1. Also used for set intersection.

**Signature:**
```python
def __and__(self, other):
    return type(self)(self.value & other.value)

def __rand__(self, other):
    return self.__and__(other)

def __iand__(self, other):
    self.value &= other.value
    return self
```

**Called automatically when:**
```python
a & b    # __and__
a &= b   # __iand__
```

**Relationships:** Reflected: `__rand__` · In-place: `__iand__`
"""