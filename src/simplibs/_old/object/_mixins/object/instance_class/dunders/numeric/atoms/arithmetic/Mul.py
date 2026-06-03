from typing import Any
from .....methods.modificators import ModifyInstance


class MulMixin(ModifyInstance):
    __slots__ = ()


    def __mul__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = self.value * other_value
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented


    def __rmul__(self, other: Any) -> Any:
        return self.__mul__(other)



__DOCT__ = """
**Purpose:**
Implements the `*` multiplication operator. Also used for repetition (`"x" * 3`).

**Signature:**
```python
def __mul__(self, other):
    return NotImplemented   # or type(self)(self.value * other)

def __rmul__(self, other):
    return self.__mul__(other)
```

**Called automatically when:**
```python
a * b   # calls a.__mul__(b); if NotImplemented → b.__rmul__(a)
```

**Relationships:** Reflected: `__rmul__` · In-place: `__imul__`
"""