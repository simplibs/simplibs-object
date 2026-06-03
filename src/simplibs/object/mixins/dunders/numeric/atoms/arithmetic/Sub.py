from typing import Any
from .....methods.modificators import ModifyInstance


class SubMixin(ModifyInstance):

    __slots__ = ()

    # Očekává
    value: Any

    def __sub__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = self.value - other_value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented


    def __rsub__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = other_value - self.value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements the `-` binary subtraction operator.

**Signature:**
```python
def __sub__(self, other):
    if not isinstance(other, type(self)):
        return NotImplemented
    return type(self)(self.value - other.value)

def __rsub__(self, other):
    return type(self)(other - self.value)
```

**Called automatically when:**
```python
a - b   # calls a.__sub__(b); if NotImplemented → b.__rsub__(a)
```

**Relationships:** Reflected: `__rsub__` · In-place: `__isub__`
"""