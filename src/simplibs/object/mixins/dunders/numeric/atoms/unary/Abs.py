from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class AbsMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __abs__(self):
        try:
            return self.create_modified_instance(value=abs(self.value))
        except TypeError:
            return NotImplemented


__DOCT__ = """
**Purpose:**
Implements `abs(obj)`. For numeric types this returns the absolute (non-negative) value.
For complex numbers, it returns the magnitude. Can be overloaded for vectors (norm),
matrices, etc.

**Signature:**
```python
def __abs__(self):
    return type(self)(abs(self.value))
```

**Called automatically when:**
```python
abs(obj)   # calls obj.__abs__()
```

**Relationships:** Related to `__neg__` and `__pos__`. `abs(x)` ≡ `x if x >= 0 else -x` conceptually.
"""