from typing import Any
from .....methods.modificators import ModifyInstance


class DivMixin(ModifyInstance):
    __slots__ = ()


    def __truediv__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = self.value / other_value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented


    def __rtruediv__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = other_value / self.value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented


__DOCT__ = """
**Purpose:**
Implements the `/` true division operator. Always returns a float (or float-like) result.
Distinct from `//` floor division.

**Signature:**
```python
def __truediv__(self, other):
    if other == 0:
        raise ZeroDivisionError
    return type(self)(self.value / other)

def __rtruediv__(self, other):
    return type(self)(other / self.value)
```

**Called automatically when:**
```python
a / b   # calls a.__truediv__(b); if NotImplemented → b.__rtruediv__(a)
```

**Relationships:** Reflected: `__rtruediv__` · In-place: `__itruediv__` · Contrast: `__floordiv__`
"""