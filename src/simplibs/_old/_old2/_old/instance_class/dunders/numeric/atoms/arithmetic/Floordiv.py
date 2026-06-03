from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class FloordivMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __floordiv__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=self.value // other_value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented

    def __rfloordiv__(self, other: Any):
        try:
            other_value = getattr(other, "value", other)
            return self.create_modified_instance(value=other_value // self.value)
        except (TypeError, ZeroDivisionError):
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements the `//` floor division operator. Always rounds *down* (toward negative
infinity), not toward zero. `7 // 2 = 3`, but `-7 // 2 = -4`.

**Signature:**
```python
def __floordiv__(self, other):
    return type(self)(self.value // other)

def __rfloordiv__(self, other):
    return type(self)(other // self.value)
```

**Called automatically when:**
```python
a // b
```

**Relationships:** Reflected: `__rfloordiv__` · In-place: `__ifloordiv__` · Contrast: `__truediv__`
"""