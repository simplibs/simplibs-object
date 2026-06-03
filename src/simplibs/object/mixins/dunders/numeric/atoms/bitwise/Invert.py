from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class InvertMixin(ModifyInstance):
    __slots__ = ()

    value: Any


    def __invert__(self):
        try:
            return self.create_modified_instance(value=~self.value)
        except TypeError:
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements `~x` — the bitwise NOT (unary). Flips all bits; for integers the result is
`-(x + 1)` due to two's complement representation.

**Signature:**
```python
def __invert__(self):
    return type(self)(~self.value)
```

**Called automatically when:**
```python
~obj   # calls obj.__invert__()
```

**Relationships:**
- Unlike `__and__`, `__or__`, `__xor__` this is *unary* — takes no second operand.
- Grouped with bitwise ops because it operates on bits.
"""