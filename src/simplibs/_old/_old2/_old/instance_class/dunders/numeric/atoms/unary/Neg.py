from typing import Any
from .....methods.modificators.ModifyInstance import ModifyInstance


class NegMixin(ModifyInstance):
    __slots__ = ()

    value: Any

    def __neg__(self):
        try:
            return self.create_modified_instance(value=-self.value)
        except TypeError:
            return NotImplemented



__DOCT__ = """
**Purpose:**
Implements unary `-x` — mathematical negation. Should return a new object of the
same type with the value negated, not modify `self`.

**Signature:**
```python
def __neg__(self):
    return type(self)(-self.value)
```

**Called automatically when:**
```python
-obj   # calls obj.__neg__()
```

**Relationships:** Complementary to `__pos__`. Contrast with `__sub__` (binary).

**Example:**
```python
class Temperature:
    def __init__(self, degrees): self.degrees = degrees
    def __neg__(self): return Temperature(-self.degrees)
    def __repr__(self): return f"{self.degrees}°"

t = Temperature(5)
print(-t)   # -5°
```
"""