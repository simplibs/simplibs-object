from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class OrMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __or__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value | other_value)
        except TypeError:
            return NotImplemented

    def __ror__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value | self.value)
        except TypeError:
            return NotImplemented




__DOCT__ = """
**Purpose:**
Implements the `|` bitwise OR. Each bit is 1 if either operand has a 1 in that position.
Used for set union, and since Python 3.9 for dict merging (`{**a, **b}` → `a | b`).

**Signature:**
```python
def __or__(self, other):
    return type(self)(self.value | other.value)

def __ror__(self, other): ...
def __ior__(self, other): self.value |= other.value; return self
```

**Called automatically when:**
```python
a | b    # __or__
a |= b   # __ior__
```

**Relationships:** Reflected: `__ror__` · In-place: `__ior__`
"""