from typing import Any
from .....methods.modificators import ModifyInstance


class AddMixin(ModifyInstance):

    __slots__ = ()

    # Očekává
    value: Any

    def __add__(self, other: Any) -> Any:
        try:
            other_value = getattr(other, "value", other)
            new_value = self.value + other_value
            # Vracíme novou instanci se stejnými metadaty, ale novou hodnotou
            return self.create_modified_instance(value=new_value)
        except TypeError:
            return NotImplemented


    def __radd__(self, other: Any) -> Any:
        return self.__add__(other)


__DOCT__ = """
**Purpose:**
Implements the `+` operator. Also commonly used for concatenation (strings, lists).
Return `NotImplemented` if the operand type is not supported — never raise `TypeError`
directly, as that prevents Python from trying the reflected method on the right operand.

**Signature:**
```python
def __add__(self, other):
    if not isinstance(other, type(self)):
        return NotImplemented
    return type(self)(self.value + other.value)

def __radd__(self, other):   # optional reflected variant
    return self.__add__(other)
```

**Called automatically when:**
```python
a + b   # calls a.__add__(b); if NotImplemented → b.__radd__(a)
```

**Relationships:**
- Reflected: `__radd__`
- In-place: `__iadd__`
- String concatenation overloads `__add__` on `str`; list concatenation on `list`.

**Example:**
```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, other):
        if not isinstance(other, Vector): return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self): return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4))  # Vector(4, 6)
```
"""